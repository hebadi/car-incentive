"""Sync vehicle catalog from fueleconomy.gov (free) + MarketCheck (paid, optional).

Primary source: fueleconomy.gov REST API (DOE/EPA)
  - Free, no API key, complete make/model/year/fuel-type data
  - Uses baseModel field for clean model names (not trim-level variants)
  - atvType field for accurate BEV/PHEV/HEV/ICE classification

Secondary source: MarketCheck API (if key configured)
  - Supplements with real dealer inventory data
  - Catches models that haven't received EPA ratings yet

Usage:
    python -m app.tasks.sync_vehicle_catalog              # full sync (fueleconomy.gov + MarketCheck)
    python -m app.tasks.sync_vehicle_catalog --seed        # seed from constants only
    python -m app.tasks.sync_vehicle_catalog --fueleco     # fueleconomy.gov only
"""
from __future__ import annotations

import asyncio
import logging
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

import httpx
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.services.marketcheck_client import MarketCheckClient

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# fueleconomy.gov API
# ---------------------------------------------------------------------------
_FUELECO_BASE = "https://fueleconomy.gov/ws/rest/vehicle"

# atvType -> our fuel code
_ATV_TYPE_MAP: Dict[str, str] = {
    "EV": "BEV",
    "Plug-in Hybrid": "PHEV",
    "Hybrid": "HEV",
    "Diesel": "ICE",
    "FFV": "ICE",       # flex-fuel
    "CNG": "ICE",       # compressed natural gas
}

# MarketCheck fuel type mapping
_MC_FUEL_MAP: Dict[str, str] = {
    "electric": "BEV",
    "plug-in hybrid": "PHEV",
    "plug_in_hybrid": "PHEV",
    "phev": "PHEV",
    "hydrogen": "FCEV",
    "fuel cell": "FCEV",
    "hybrid": "HEV",
    "gasoline": "ICE",
    "diesel": "ICE",
    "flex fuel": "ICE",
    "flex": "ICE",
    "gas": "ICE",
}

MAKES = [
    "Acura", "Audi", "BMW", "Buick", "Cadillac", "Chevrolet", "Chrysler",
    "Dodge", "Fiat", "Ford", "Genesis", "GMC", "Honda", "Hyundai",
    "Infiniti", "Jaguar", "Jeep", "Kia", "Land Rover", "Lexus",
    "Lincoln", "Lucid", "Mazda", "Mercedes-Benz", "Mini", "Mitsubishi",
    "Nissan", "Polestar", "Porsche", "Ram", "Rivian", "Subaru",
    "Tesla", "Toyota", "Volkswagen", "Volvo",
]

# Hardcoded seed data (fallback when no external API is reachable)
_SEED_MODELS: Dict[str, List[Tuple[str, List[str]]]] = {
    "Acura": [("Integra", ["ICE"]), ("MDX", ["ICE"]), ("RDX", ["ICE"]), ("TLX", ["ICE"]), ("ZDX", ["BEV"])],
    "Audi": [("A4", ["ICE"]), ("e-tron GT", ["BEV"]), ("Q4 e-tron", ["BEV"]), ("Q6 e-tron", ["BEV"]), ("Q8 e-tron", ["BEV"])],
    "BMW": [("i4", ["BEV"]), ("i5", ["BEV"]), ("i7", ["BEV"]), ("iX", ["BEV"]), ("X5 xDrive50e", ["PHEV"])],
    "Chevrolet": [("Blazer EV", ["BEV"]), ("Bolt EUV", ["BEV"]), ("Equinox EV", ["BEV"]), ("Silverado EV", ["BEV"]), ("Silverado", ["ICE"]), ("Tahoe", ["ICE"])],
    "Ford": [("F-150 Lightning", ["BEV"]), ("Mustang Mach-E", ["BEV"]), ("Escape PHEV", ["PHEV"]), ("F-150", ["ICE"]), ("Bronco", ["ICE"])],
    "Genesis": [("Electrified G80", ["BEV"]), ("Electrified GV70", ["BEV"]), ("GV60", ["BEV"]), ("G70", ["ICE"])],
    "Honda": [("Prologue", ["BEV"]), ("Accord", ["ICE"]), ("Civic", ["ICE"]), ("CR-V", ["ICE"]), ("CR-V PHEV", ["PHEV"])],
    "Hyundai": [("IONIQ 5", ["BEV"]), ("IONIQ 6", ["BEV"]), ("IONIQ 9", ["BEV"]), ("Kona Electric", ["BEV"]), ("Tucson PHEV", ["PHEV"]), ("Santa Fe", ["ICE"])],
    "Kia": [("EV6", ["BEV"]), ("EV9", ["BEV"]), ("Niro EV", ["BEV"]), ("Niro PHEV", ["PHEV"]), ("Sportage", ["ICE"]), ("Telluride", ["ICE"])],
    "Mercedes-Benz": [("EQE", ["BEV"]), ("EQE SUV", ["BEV"]), ("EQS", ["BEV"]), ("EQS SUV", ["BEV"]), ("C-Class", ["ICE"])],
    "Nissan": [("Ariya", ["BEV"]), ("LEAF", ["BEV"]), ("Altima", ["ICE"]), ("Rogue", ["ICE"])],
    "Rivian": [("R1S", ["BEV"]), ("R1T", ["BEV"]), ("R2", ["BEV"])],
    "Subaru": [("Solterra", ["BEV"]), ("Crosstrek PHEV", ["PHEV"]), ("Outback", ["ICE"]), ("Forester", ["ICE"])],
    "Tesla": [("Model 3", ["BEV"]), ("Model Y", ["BEV"]), ("Model S", ["BEV"]), ("Model X", ["BEV"]), ("Cybertruck", ["BEV"])],
    "Toyota": [
        ("bZ", ["BEV"]), ("C-HR", ["BEV"]), ("Camry", ["ICE"]), ("Corolla", ["ICE"]),
        ("Crown", ["ICE"]), ("Grand Highlander", ["ICE"]), ("GR86", ["ICE"]),
        ("GR Corolla", ["ICE"]), ("GR Supra", ["ICE"]), ("Highlander", ["ICE"]),
        ("Land Cruiser", ["ICE"]), ("Prius", ["ICE"]), ("Prius Prime", ["PHEV"]),
        ("RAV4", ["ICE"]), ("RAV4 Prime", ["PHEV"]), ("Sequoia", ["ICE"]),
        ("Tacoma", ["ICE"]), ("Tundra", ["ICE"]), ("Venza", ["ICE"]), ("4Runner", ["ICE"]),
    ],
    "Volkswagen": [("ID.4", ["BEV"]), ("ID.Buzz", ["BEV"]), ("Atlas", ["ICE"]), ("Jetta", ["ICE"]), ("Taos", ["ICE"]), ("Tiguan", ["ICE"])],
    "Volvo": [("C40 Recharge", ["BEV"]), ("EX30", ["BEV"]), ("EX90", ["BEV"]), ("XC40 Recharge", ["BEV"]), ("XC60", ["PHEV", "ICE"]), ("XC90", ["PHEV", "ICE"])],
    "Polestar": [("Polestar 2", ["BEV"]), ("Polestar 3", ["BEV"]), ("Polestar 4", ["BEV"])],
    "Lucid": [("Air", ["BEV"]), ("Gravity", ["BEV"])],
}


def _normalize_mc_fuel(raw: Optional[str]) -> str:
    """Map MarketCheck fuel type string to our standard code."""
    if not raw:
        return "ICE"
    return _MC_FUEL_MAP.get(raw.lower().strip(), "ICE")


def _normalize_model_name(model: str, make: str = "") -> str:
    """Clean up model name casing quirks from external sources."""
    # MarketCheck sometimes returns all-caps: "CIVIC" -> "Civic"
    if model.isupper() and len(model) > 3 and "-" not in model:
        model = model.title()
    return model


# Polestar EPA models are just "2", "3", "4" — prepend make name
# Also handles any other makes where baseModel is just a number
_MAKE_PREFIX_MODELS: Dict[str, Dict[str, str]] = {
    "Polestar": {"2": "Polestar 2", "3": "Polestar 3", "4": "Polestar 4"},
}


def _normalize_base_model(base_model: str, make: str) -> str:
    """Normalize fueleconomy.gov baseModel to match our naming conventions."""
    overrides = _MAKE_PREFIX_MODELS.get(make, {})
    if base_model in overrides:
        return overrides[base_model]
    # GR 86 vs GR86
    if make == "Toyota" and base_model == "GR 86":
        return "GR86"
    return base_model


def _ensure_list(menu_item: Any) -> list:
    """Handle fueleconomy.gov menuItem being a single object or array."""
    if menu_item is None:
        return []
    if isinstance(menu_item, list):
        return menu_item
    return [menu_item]


# ---------------------------------------------------------------------------
# fueleconomy.gov sync
# ---------------------------------------------------------------------------

def _fueleco_get_json(client: httpx.Client, path: str, params: Optional[dict] = None) -> Any:
    """GET from fueleconomy.gov with JSON Accept header."""
    resp = client.get(
        f"{_FUELECO_BASE}{path}",
        params=params or {},
        headers={"Accept": "application/json"},
    )
    resp.raise_for_status()
    return resp.json()


def _sync_from_fueleconomy() -> Dict[Tuple[str, str, int], Set[str]]:
    """Pull make/model/fuel data from fueleconomy.gov for current + next year.

    Returns a dict mapping (make, baseModel, year) -> set of fuel codes.
    """
    catalog: Dict[Tuple[str, str, int], Set[str]] = defaultdict(set)
    current_year = datetime.now().year
    years = [current_year - 1, current_year]

    with httpx.Client(timeout=30) as client:
        for year in years:
            # Get all makes for this year
            try:
                data = _fueleco_get_json(client, "/menu/make", {"year": year})
                if data is None:
                    logger.info("fueleconomy.gov: no data for year %d — skipping", year)
                    continue
            except Exception as exc:
                logger.warning("fueleconomy.gov: failed to get makes for %d: %s", year, exc)
                continue

            api_makes = _ensure_list(data.get("menuItem", []))
            if not api_makes:
                logger.info("fueleconomy.gov: no makes for year %d — skipping", year)
                continue
            # Filter to our tracked makes (case-insensitive match)
            our_makes_lower = {m.lower(): m for m in MAKES}

            for make_item in api_makes:
                api_make = make_item.get("value", "")
                canonical_make = our_makes_lower.get(api_make.lower())
                if not canonical_make:
                    continue

                # Get models for this make+year
                try:
                    model_data = _fueleco_get_json(
                        client, "/menu/model", {"year": year, "make": api_make}
                    )
                except Exception as exc:
                    logger.warning("fueleconomy.gov: failed to get models for %s %d: %s", api_make, year, exc)
                    continue

                model_items = _ensure_list(model_data.get("menuItem", []))

                # For each model variant, get the vehicle ID and fetch fuel type
                for model_item in model_items:
                    model_name = model_item.get("value", "")
                    if not model_name:
                        continue

                    # Get vehicle option IDs for this specific model
                    try:
                        options_data = _fueleco_get_json(
                            client, "/menu/options",
                            {"year": year, "make": api_make, "model": model_name},
                        )
                    except Exception:
                        continue

                    option_items = _ensure_list(options_data.get("menuItem"))
                    if not option_items:
                        continue

                    # Fetch first vehicle ID to get baseModel + atvType
                    vid = option_items[0].get("value")
                    if not vid:
                        continue

                    try:
                        vehicle = _fueleco_get_json(client, f"/{vid}")
                    except Exception:
                        continue

                    base_model = vehicle.get("baseModel", model_name)
                    base_model = _normalize_base_model(base_model, canonical_make)
                    atv_type = vehicle.get("atvType", "")

                    # Map atvType to our fuel code
                    fuel = _ATV_TYPE_MAP.get(atv_type, "ICE")

                    key = (canonical_make, base_model, year)
                    catalog[key].add(fuel)

                    # Be polite — small delay between detail requests
                    time.sleep(0.1)

            logger.info("fueleconomy.gov: synced %d for year %d", len(api_makes), year)

    logger.info("fueleconomy.gov: total unique models: %d", len(catalog))
    return catalog


# ---------------------------------------------------------------------------
# MarketCheck sync (supplements fueleconomy.gov)
# ---------------------------------------------------------------------------

def _sync_from_marketcheck_data() -> Dict[Tuple[str, str, int], Set[str]]:
    """Pull vehicle listings from MarketCheck. Returns same format as fueleco."""
    client = MarketCheckClient()
    if client.is_mock:
        return {}

    catalog: Dict[Tuple[str, str, int], Set[str]] = defaultdict(set)
    current_year = datetime.now().year

    for make in MAKES:
        try:
            listings = client.get_vehicle_listings(
                make=make, inventory_type="new", rows=50,
            )
            for listing in listings:
                if not listing.model or listing.year < current_year - 1:
                    continue
                model_name = _normalize_model_name(listing.model)
                fuel = _normalize_mc_fuel(listing.fuel_type)
                key = (listing.make, model_name, listing.year)
                catalog[key].add(fuel)
            logger.info("MarketCheck: synced %s — %d listings", make, len(listings))
        except Exception as exc:
            logger.warning("MarketCheck: failed %s — %s", make, exc)

    return catalog


# ---------------------------------------------------------------------------
# DB upsert
# ---------------------------------------------------------------------------

async def _upsert_catalog(
    session: AsyncSession,
    catalog: Dict[Tuple[str, str, int], Set[str]],
    source: str,
) -> int:
    """Upsert catalog entries and return count."""
    now = datetime.now(timezone.utc)
    upserted = 0

    for (make, model, year), fuel_types in catalog.items():
        fuel_list = sorted(fuel_types)
        await session.execute(
            text("""
                INSERT INTO vehicle_catalog (make, model, year, fuel_types, is_active, last_seen_at, source)
                VALUES (:make, :model, :year, :fuel_types, true, :now, :source)
                ON CONFLICT (make, model, year)
                DO UPDATE SET
                    fuel_types = ARRAY(
                        SELECT DISTINCT unnest(vehicle_catalog.fuel_types || EXCLUDED.fuel_types)
                    ),
                    is_active = true,
                    last_seen_at = :now,
                    updated_at = :now
            """),
            {"make": make, "model": model, "year": year, "fuel_types": fuel_list, "now": now, "source": source},
        )
        upserted += 1

    return upserted


async def _deactivate_stale(session: AsyncSession) -> None:
    """Deactivate models not seen in 90 days."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=90)
    await session.execute(
        text("UPDATE vehicle_catalog SET is_active = false, updated_at = :now WHERE last_seen_at < :cutoff AND is_active = true"),
        {"now": now, "cutoff": cutoff},
    )


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------

async def _seed_from_constants(session: AsyncSession) -> dict:
    """Seed vehicle_catalog from hardcoded data."""
    now = datetime.now(timezone.utc)
    current_year = datetime.now().year
    catalog: Dict[Tuple[str, str, int], Set[str]] = {}

    for make, models in _SEED_MODELS.items():
        for model_name, fuel_types in models:
            catalog[(make, model_name, current_year)] = set(fuel_types)

    upserted = await _upsert_catalog(session, catalog, "seed")
    await session.commit()
    return {"upserted": upserted, "errors": [], "source": "seed"}


async def _sync_full(session: AsyncSession, fueleco_only: bool = False) -> dict:
    """Full sync: fueleconomy.gov (primary) + MarketCheck (secondary)."""
    results = {"fueleco": 0, "marketcheck": 0, "errors": []}

    # 1. fueleconomy.gov (free, authoritative)
    try:
        fueleco_catalog = _sync_from_fueleconomy()
        results["fueleco"] = await _upsert_catalog(session, fueleco_catalog, "fueleconomy.gov")
        logger.info("fueleconomy.gov: upserted %d models", results["fueleco"])
    except Exception as exc:
        logger.error("fueleconomy.gov sync failed: %s", exc)
        results["errors"].append(f"fueleconomy.gov: {exc}")

    # 2. MarketCheck (supplements with inventory-based models)
    if not fueleco_only:
        try:
            mc_catalog = _sync_from_marketcheck_data()
            if mc_catalog:
                results["marketcheck"] = await _upsert_catalog(session, mc_catalog, "marketcheck")
                logger.info("MarketCheck: upserted %d models", results["marketcheck"])
        except Exception as exc:
            logger.warning("MarketCheck sync failed (non-fatal): %s", exc)
            results["errors"].append(f"marketcheck: {exc}")

    # 3. If both sources returned nothing, seed from constants
    if results["fueleco"] == 0 and results["marketcheck"] == 0:
        logger.warning("No external data — falling back to seed constants")
        seed_result = await _seed_from_constants(session)
        results["seed_fallback"] = seed_result["upserted"]

    await _deactivate_stale(session)
    await session.commit()

    total = results["fueleco"] + results["marketcheck"]
    logger.info("Vehicle catalog sync complete: %d total models upserted", total)
    return results


async def _sync_async(seed_only: bool = False, fueleco_only: bool = False) -> dict:
    """Main async entry point."""
    engine = create_async_engine(settings.database_url, echo=False)
    async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session_factory() as session:
        if seed_only:
            result = await _seed_from_constants(session)
        else:
            result = await _sync_full(session, fueleco_only=fueleco_only)

    await engine.dispose()
    return result


def sync_vehicle_catalog(seed_only: bool = False, fueleco_only: bool = False) -> dict:
    """Synchronous entry point for cron/Celery."""
    return asyncio.run(_sync_async(seed_only=seed_only, fueleco_only=fueleco_only))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed_flag = "--seed" in sys.argv
    fueleco_flag = "--fueleco" in sys.argv
    result = sync_vehicle_catalog(seed_only=seed_flag, fueleco_only=fueleco_flag)
    print(f"Done: {result}")
