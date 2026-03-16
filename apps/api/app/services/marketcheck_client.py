"""
MarketCheck API client for vehicle listing and market pricing data.

Provides auth, rate limiting, error handling, and response parsing.
Uses the /v2/search/car/active endpoint for real vehicle inventory data.

Supports a stub/mock mode when no API key is configured.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

BASE_URL = "https://mc-api.marketcheck.com/v2"

# Rate limit: max 5 requests per second
_RATE_LIMIT_INTERVAL = 0.2
_last_request_time = 0.0


@dataclass
class MarketCheckIncentive:
    """Parsed incentive from MarketCheck API response."""
    name: str
    make: str
    model: str | None
    trim: str | None
    incentive_type: str  # cash, lease, apr
    amount: float | None
    max_amount: float | None
    percentage: float | None
    monthly_payment: float | None
    lease_term: int | None
    due_at_signing: float | None
    start_date: str | None
    end_date: str | None
    description: str
    disclaimer: str | None
    source_url: str
    photo_url: str | None


@dataclass
class MarketCheckVehicleListing:
    """Parsed vehicle listing from MarketCheck API response."""
    vin: str
    make: str
    model: str
    year: int
    trim: str | None
    price: float | None
    msrp: float | None
    miles: int | None
    dealer_name: str | None
    dealer_city: str | None
    dealer_state: str | None
    dealer_zip: str | None
    fuel_type: str | None
    listing_url: str | None
    photo_url: str | None
    inventory_type: str | None


@dataclass
class MarketPricing:
    """Aggregated market pricing for a make/model."""
    make: str
    model: str
    total_listings: int
    avg_price: float | None
    min_price: float | None
    max_price: float | None
    avg_msrp: float | None
    sample_listings: list[MarketCheckVehicleListing]


# ---- Stub data for development ----

_STUB_INCENTIVES: list[dict] = [
    {
        "name": "Hyundai IONIQ 5 National Bonus Cash",
        "make": "Hyundai",
        "model": "IONIQ 5",
        "incentive_type": "cash",
        "amount": 2000,
        "max_amount": 2000,
        "percentage": None,
        "start_date": "2026-01-01",
        "end_date": "2026-03-31",
        "description": "National bonus cash on 2026 IONIQ 5",
    },
    {
        "name": "Toyota RAV4 Prime APR Special",
        "make": "Toyota",
        "model": "RAV4 Prime",
        "incentive_type": "apr",
        "amount": None,
        "max_amount": None,
        "percentage": 2.9,
        "start_date": "2026-01-01",
        "end_date": "2026-06-30",
        "description": "2.9% APR for 60 months on RAV4 Prime",
    },
]

_STUB_LISTINGS: list[dict] = [
    {
        "vin": "5YJ3E1EA1RF000001",
        "make": "Tesla",
        "model": "Model Y",
        "year": 2026,
        "trim": "Long Range",
        "price": 47990,
        "msrp": 49990,
        "miles": 0,
        "dealer_name": "Tesla Fremont",
        "dealer_city": "Fremont",
        "dealer_state": "CA",
        "dealer_zip": "94538",
        "fuel_type": "Electric",
        "listing_url": None,
        "photo_url": None,
        "inventory_type": "new",
    },
]


class MarketCheckClient:
    """Client for the MarketCheck API with rate limiting and mock mode."""

    def __init__(self, api_key: str | None = None):
        self._api_key = api_key or settings.marketcheck_api_key
        self._mock = not bool(self._api_key)
        if self._mock:
            logger.warning("MarketCheck API key not configured -- running in stub/mock mode")

    @property
    def is_mock(self) -> bool:
        return self._mock

    def _rate_limit(self) -> None:
        global _last_request_time
        elapsed = time.monotonic() - _last_request_time
        if elapsed < _RATE_LIMIT_INTERVAL:
            time.sleep(_RATE_LIMIT_INTERVAL - elapsed)
        _last_request_time = time.monotonic()

    def _get(self, path: str, params: dict | None = None) -> dict:
        """Make a rate-limited GET request to the MarketCheck API."""
        if self._mock:
            raise RuntimeError("Cannot make real API calls in mock mode")

        self._rate_limit()
        params = params or {}
        params["api_key"] = self._api_key

        with httpx.Client(timeout=30) as client:
            resp = client.get(f"{BASE_URL}{path}", params=params)
            resp.raise_for_status()
            return resp.json()

    # ---- Public methods ----

    def get_oem_incentives(
        self, make: str, model: str | None = None, zip_code: str | None = None,
        offer_type: str | None = None, rows: int = 50,
    ) -> list[MarketCheckIncentive]:
        """Fetch OEM incentives via /v2/search/car/incentive/oem endpoint."""
        if self._mock:
            results = []
            for stub in _STUB_INCENTIVES:
                if stub["make"].lower() == make.lower():
                    if model and stub.get("model") and stub["model"].lower() != model.lower():
                        continue
                    results.append(
                        MarketCheckIncentive(
                            source_url="https://www.marketcheck.com",
                            trim=None, monthly_payment=None, lease_term=None,
                            due_at_signing=None, disclaimer=None, photo_url=None,
                            **stub,
                        )
                    )
            return results

        params: dict = {"make": make, "rows": rows}
        if model:
            params["model"] = model
        if zip_code:
            params["zip"] = zip_code
        if offer_type:
            params["offer_type"] = offer_type

        data = self._get("/search/car/incentive/oem", params)
        incentives = []
        seen_keys: set[str] = set()  # dedupe by make+model+trim+type+amount

        for item in data.get("listings", []):
            offer = item.get("offer") or {}
            vehicles = offer.get("vehicles") or [{}]
            v = vehicles[0] if vehicles else {}
            amounts = offer.get("amounts") or [{}]
            a = amounts[0] if amounts else {}

            inc_make = v.get("make", make)
            inc_model = v.get("model")
            inc_trim = v.get("trim")
            inc_type = offer.get("offer_type", "cash")

            # Extract amount based on offer type
            amount = None
            monthly = None
            lease_term = None
            due_at_signing = None
            percentage = None

            if inc_type == "cash":
                amount = offer.get("cashback_amount") or a.get("cash")
            elif inc_type == "lease":
                monthly = a.get("monthly")
                lease_term = a.get("term")
                due_at_signing = offer.get("due_at_signing")
            elif inc_type == "apr":
                percentage = a.get("apr")

            # Build a readable name
            titles = offer.get("titles") or []
            offers_text = offer.get("offers") or []
            if titles:
                name = f"{inc_make} {titles[0]} - {inc_type.upper()}"
            else:
                name = f"{inc_make} {inc_model or ''} {inc_trim or ''} - {inc_type.upper()}".strip()

            # Dedupe: same make+model+trim+type+amount is the same offer across regions
            dedup_key = f"{inc_make}|{inc_model}|{inc_trim}|{inc_type}|{amount}|{monthly}"
            if dedup_key in seen_keys:
                continue
            seen_keys.add(dedup_key)

            # Dates
            start_date = offer.get("valid_from")
            end_date = offer.get("valid_through")

            # Description from offers text
            description = "; ".join(offers_text) if offers_text else ""

            # Disclaimers
            disclaimers = offer.get("disclaimers") or []
            disclaimer = disclaimers[0] if disclaimers else None

            # Photo
            photos = offer.get("photo_links") or []
            photo_url = photos[0] if photos else None

            source = item.get("source", "marketcheck.com")

            incentives.append(
                MarketCheckIncentive(
                    name=name,
                    make=inc_make,
                    model=inc_model,
                    trim=inc_trim,
                    incentive_type=inc_type,
                    amount=amount,
                    max_amount=amount,
                    percentage=percentage,
                    monthly_payment=monthly,
                    lease_term=lease_term,
                    due_at_signing=due_at_signing,
                    start_date=start_date,
                    end_date=end_date,
                    description=description,
                    disclaimer=disclaimer,
                    source_url=f"https://{source}" if not source.startswith("http") else source,
                    photo_url=photo_url,
                )
            )
        return incentives

    def get_vehicle_listings(
        self,
        make: str | None = None,
        model: str | None = None,
        year: int | None = None,
        zip_code: str | None = None,
        radius: int = 50,
        fuel_type: str | None = None,
        max_price: float | None = None,
        inventory_type: str | None = None,
        rows: int = 25,
    ) -> list[MarketCheckVehicleListing]:
        """Fetch vehicle listings with optional filters."""
        if self._mock:
            results = []
            for stub in _STUB_LISTINGS:
                if make and stub["make"].lower() != make.lower():
                    continue
                if model and stub["model"].lower() != model.lower():
                    continue
                results.append(MarketCheckVehicleListing(**stub))
            return results

        params: dict = {"rows": rows}
        if make:
            params["make"] = make
        if model:
            params["model"] = model
        if year:
            params["year"] = year
        if zip_code:
            params["zip"] = zip_code
            params["radius"] = radius
        if fuel_type:
            params["fuel_type"] = fuel_type
        if max_price:
            params["price_range"] = f"0-{int(max_price)}"
        if inventory_type:
            params["inventory_type"] = inventory_type

        data = self._get("/search/car/active", params)
        listings = []
        for item in data.get("listings", []):
            dealer = item.get("dealer") or {}
            photos = (item.get("media") or {}).get("photo_links") or []
            listings.append(
                MarketCheckVehicleListing(
                    vin=item.get("vin", ""),
                    make=item.get("make", ""),
                    model=item.get("model", ""),
                    year=item.get("year", 0),
                    trim=item.get("trim"),
                    price=item.get("price"),
                    msrp=item.get("msrp"),
                    miles=item.get("miles"),
                    dealer_name=dealer.get("name"),
                    dealer_city=dealer.get("city"),
                    dealer_state=dealer.get("state"),
                    dealer_zip=dealer.get("zip"),
                    fuel_type=item.get("fuel_type"),
                    listing_url=item.get("vdp_url"),
                    photo_url=photos[0] if photos else None,
                    inventory_type=item.get("inventory_type"),
                )
            )
        return listings

    def get_market_pricing(
        self,
        make: str,
        model: str,
        zip_code: str | None = None,
        radius: int = 100,
        inventory_type: str = "new",
    ) -> MarketPricing:
        """Get aggregated market pricing for a make/model from real listings."""
        listings = self.get_vehicle_listings(
            make=make,
            model=model,
            zip_code=zip_code,
            radius=radius,
            inventory_type=inventory_type,
            rows=50,
        )

        prices = [l.price for l in listings if l.price]
        msrps = [l.msrp for l in listings if l.msrp]

        return MarketPricing(
            make=make,
            model=model,
            total_listings=len(listings),
            avg_price=round(sum(prices) / len(prices), 2) if prices else None,
            min_price=min(prices) if prices else None,
            max_price=max(prices) if prices else None,
            avg_msrp=round(sum(msrps) / len(msrps), 2) if msrps else None,
            sample_listings=listings[:5],
        )

    def incentive_to_program_dict(self, inc: MarketCheckIncentive) -> dict:
        """Convert a MarketCheckIncentive to a dict matching the incentive_programs schema."""
        if inc.incentive_type == "apr":
            value_type = "rate_reduction"
        elif inc.incentive_type == "lease":
            value_type = "fixed"  # lease deals stored as fixed amount (monthly payment)
        else:
            value_type = "fixed"

        # Map offer type to purchase type
        purchase_types = {
            "cash": ["cash"],
            "lease": ["lease"],
            "apr": ["finance"],
        }

        # Parse dates from MM/DD/YYYY to ISO
        start_date = inc.start_date
        end_date = inc.end_date
        if start_date and "/" in start_date:
            try:
                from datetime import datetime as dt
                start_date = dt.strptime(start_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            except ValueError:
                pass
        if end_date and "/" in end_date:
            try:
                from datetime import datetime as dt
                end_date = dt.strptime(end_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            except ValueError:
                pass

        vehicle_criteria: dict = {"make": inc.make}
        if inc.model:
            vehicle_criteria["model"] = inc.model
        if inc.trim:
            vehicle_criteria["trim"] = inc.trim

        return {
            "name": inc.name,
            "type": "manufacturer",
            "source_authority": f"{inc.make} (via MarketCheck)",
            "data_source": "marketcheck",
            "geographic_scope": "national",
            "eligible_states": [],
            "eligible_zips": [],
            "vehicle_criteria": vehicle_criteria,
            "buyer_criteria": {},
            "incentive_value_type": value_type,
            "incentive_amount": inc.amount,
            "incentive_max_amount": inc.max_amount,
            "incentive_percentage": inc.percentage,
            "stackable_with": [],
            "mutually_exclusive_with": [],
            "eligible_purchase_types": purchase_types.get(inc.incentive_type, ["cash", "finance", "lease"]),
            "start_date": start_date,
            "end_date": end_date,
            "application_deadline": None,
            "funding_status": "open",
            "claim_mechanism": "lease_reduction" if inc.incentive_type == "lease" else "point_of_sale",
            "last_verified": datetime.now(timezone.utc).isoformat(),
            "source_url": inc.source_url,
            "confidence_score": 0.95,
            "is_active": True,
            "description": inc.description,
            "disclaimer": inc.disclaimer,
        }
