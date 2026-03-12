from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.incentive_program import IncentiveProgram
from app.schemas.incentives import (
    CalculateIncentivesRequest,
    CalculateIncentivesResponse,
    IncentiveSummary,
    IncentiveProgramResponse,
    IncentiveListResponse,
)
from app.services.incentive_matcher import (
    match_incentives,
    filter_by_geography,
    compute_value,
    resolve_stacking,
)
from app.services.marketcheck_client import MarketCheckClient

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/calculate", response_model=CalculateIncentivesResponse)
async def calculate_incentives(
    request: CalculateIncentivesRequest,
    db: AsyncSession = Depends(get_db),
):
    """Calculate applicable incentives for a buyer/vehicle/location combination."""
    result = await match_incentives(
        db=db,
        zip_code=request.zip_code,
        vehicle_interest=request.vehicle_interest.model_dump(exclude_none=True),
        buyer_profile=request.buyer_profile.model_dump(exclude_none=True),
    )

    incentive_summaries = [
        IncentiveSummary(
            id=inc["id"],
            name=inc["name"],
            type=inc["type"],
            amount=inc["amount"],
            claim_mechanism=inc["claim_mechanism"],
            confidence_score=inc["confidence_score"],
            source_url=inc.get("source_url"),
            funding_status=inc.get("funding_status"),
            end_date=inc.get("end_date"),
            last_verified=inc.get("last_verified"),
            eligible_purchase_types=inc.get("eligible_purchase_types", ["cash", "finance", "lease"]),
            claim_steps=inc.get("claim_steps", []),
        )
        for inc in result["incentives"]
    ]

    return CalculateIncentivesResponse(
        incentives=incentive_summaries,
        total_savings=result["total_savings"],
        confidence=result["confidence"],
        disclaimers=result["disclaimers"],
    )


@router.get("/top-by-zip")
async def top_incentives_by_zip(
    zip_code: str = Query(..., min_length=5, max_length=5, pattern=r"^\d{5}$"),
    db: AsyncSession = Depends(get_db),
):
    """Find vehicles with the highest total incentives for a given ZIP code.

    Returns makes ranked by total stackable savings, grouped by purchase type
    (cash, finance, lease) like Edmunds-style layout.
    """
    BLOCKED_SOURCES = {"https://www.marketcheck.com", "https://www.marketcheck.com/"}
    MIN_CONFIDENCE = 0.4  # Filter out speculative/low-confidence incentives

    # Load all active, credibly-sourced incentives
    stmt = select(IncentiveProgram).where(
        IncentiveProgram.is_active.is_(True),
        IncentiveProgram.funding_status.in_(["open", "waitlisted"]),
    )
    result = await db.execute(stmt)
    all_incentives = [
        inc for inc in result.scalars().all()
        if inc.source_url not in BLOCKED_SOURCES
        and inc.confidence_score >= MIN_CONFIDENCE
    ]

    # Filter to those available in the user's ZIP
    geo_matched = filter_by_geography(all_incentives, zip_code)

    # Group incentives by make (extracted from vehicle_criteria)
    # Also collect "universal" incentives (no make restriction) that apply to any vehicle
    make_incentives: dict[str, list] = {}
    universal_incentives: list = []

    for inc in geo_matched:
        criteria = inc.vehicle_criteria or {}
        makes = criteria.get("make", [])
        if isinstance(makes, str):
            makes = [makes]

        # Skip charger programs
        if criteria.get("category") == "charger_installation":
            continue

        # Skip model-specific incentives when grouping by make
        # (they'll still be included for that make but only if no model filter mismatches)
        if not makes:
            universal_incentives.append(inc)
        else:
            for make in makes:
                make_incentives.setdefault(make, []).append(inc)

    def _build_purchase_type_breakdown(
        stacked_incentives: list, make: str
    ) -> dict:
        """Group incentives by purchase type and compute totals per type."""
        purchase_groups: dict[str, list] = {"cash": [], "finance": [], "lease": []}

        for inc in stacked_incentives:
            value = compute_value(inc, {"make": make})
            if value <= 0:
                continue

            detail = {
                "id": str(inc.id),
                "name": inc.name,
                "type": inc.type,
                "amount": round(value, 2),
                "sourceUrl": inc.source_url,
                "claimMechanism": inc.claim_mechanism,
                "lastVerified": inc.last_verified.isoformat() if inc.last_verified else None,
                "endDate": inc.end_date.isoformat() if inc.end_date else None,
                "claimSteps": inc.claim_steps or [],
            }

            purchase_types = getattr(inc, "eligible_purchase_types", None) or ["cash", "finance", "lease"]
            for pt in purchase_types:
                if pt in purchase_groups:
                    purchase_groups[pt].append(detail)

        # Build per-type result
        result_by_type = {}
        for pt, details in purchase_groups.items():
            if not details:
                continue
            # Deduplicate (same incentive can appear if it applies to multiple types)
            seen_ids = set()
            unique = []
            for d in details:
                if d["id"] not in seen_ids:
                    seen_ids.add(d["id"])
                    unique.append(d)
            unique.sort(key=lambda x: x["amount"], reverse=True)
            result_by_type[pt] = {
                "incentives": unique,
                "total": round(sum(d["amount"] for d in unique), 2),
                "count": len(unique),
            }

        return result_by_type

    # For each make, compute total savings (make-specific + universal incentives)
    make_results = []
    for make, incentives in make_incentives.items():
        # Filter out model-specific incentives that don't match this make's general listing
        # (e.g., Santa Fe APR shouldn't appear under generic "Hyundai" when it has model restrictions)
        filtered = []
        for inc in incentives:
            criteria = inc.vehicle_criteria or {}
            models = criteria.get("models", []) or criteria.get("model", [])
            if isinstance(models, str):
                models = [models]
            # If incentive is model-specific, note it but still include (the make matched)
            filtered.append(inc)

        combined = filtered + universal_incentives
        stacked = resolve_stacking(combined)

        # Build flat list for backward compat + purchase type breakdown
        purchase_breakdown = _build_purchase_type_breakdown(stacked, make)

        if not purchase_breakdown:
            continue

        # Best purchase type total (what a buyer would actually get picking the best path)
        best_total = max(pt["total"] for pt in purchase_breakdown.values())

        # Flat incentive list (union of all purchase types, deduplicated)
        all_details = {}
        for pt_data in purchase_breakdown.values():
            for inc in pt_data["incentives"]:
                if inc["id"] not in all_details:
                    all_details[inc["id"]] = inc
        flat_incentives = sorted(all_details.values(), key=lambda x: x["amount"], reverse=True)

        make_results.append({
            "make": make,
            "totalSavings": round(best_total, 2),
            "incentiveCount": len(flat_incentives),
            "incentives": flat_incentives,
            "byPurchaseType": purchase_breakdown,
        })

    # Sort by total savings descending
    make_results.sort(key=lambda x: x["totalSavings"], reverse=True)

    return {
        "zipCode": zip_code,
        "results": make_results,
    }


@router.get("/vehicle-photo")
async def vehicle_photo(
    make: str = Query(..., min_length=1),
    model: str = Query(..., min_length=1),
):
    """Get a real photo for a vehicle from Wikipedia (free, no watermark)."""
    import httpx

    headers = {"User-Agent": "IncentiveDrive/1.0 (car incentive calculator)"}

    async def _get_photo_from_title(title: str) -> str | None:
        """Fetch the original image URL from a Wikipedia page summary."""
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code != 200:
                return None
            data = resp.json()
            img = data.get("originalimage") or data.get("thumbnail")
            return img.get("source") if img else None

    async def _search_wikipedia(query: str) -> str | None:
        """Search Wikipedia and return the first matching article title."""
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srnamespace": "0",
            "srlimit": "3",
            "format": "json",
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params, headers=headers)
            if resp.status_code != 200:
                return None
            results = resp.json().get("query", {}).get("search", [])
            return results[0]["title"] if results else None

    try:
        # Try direct title patterns first (most common Wikipedia naming)
        slug = f"{make}_{model}".replace(" ", "_")
        for title in [slug, f"{slug}_(car)", f"{slug}_(automobile)"]:
            photo = await _get_photo_from_title(title)
            if photo:
                return {"photoUrl": photo}

        # Fall back to Wikipedia search
        search_title = await _search_wikipedia(f"{make} {model} car")
        if search_title:
            photo = await _get_photo_from_title(search_title.replace(" ", "_"))
            if photo:
                return {"photoUrl": photo}

        return {"photoUrl": None}
    except Exception as e:
        logger.error("Vehicle photo error: %s", e)
        return {"photoUrl": None}


@router.get("/{state}", response_model=IncentiveListResponse)
async def list_incentives_by_state(
    state: str = Path(..., min_length=2, max_length=2, pattern=r"^[A-Z]{2}$"),
    db: AsyncSession = Depends(get_db),
):
    """List all active incentives for a state."""
    stmt = select(IncentiveProgram).where(
        IncentiveProgram.is_active.is_(True),
        IncentiveProgram.eligible_states.any(state),
    )
    result = await db.execute(stmt)
    programs = result.scalars().all()

    # Also include national incentives
    stmt_national = select(IncentiveProgram).where(
        IncentiveProgram.is_active.is_(True),
        IncentiveProgram.geographic_scope == "national",
    )
    result_national = await db.execute(stmt_national)
    national_programs = result_national.scalars().all()

    all_programs = list(programs) + list(national_programs)
    # Deduplicate by id
    seen = set()
    unique = []
    for p in all_programs:
        if p.id not in seen:
            seen.add(p.id)
            unique.append(p)

    incentive_responses = [
        IncentiveProgramResponse(
            id=str(p.id),
            name=p.name,
            type=p.type,
            source_authority=p.source_authority,
            geographic_scope=p.geographic_scope,
            incentive_value_type=p.incentive_value_type,
            incentive_amount=float(p.incentive_amount) if p.incentive_amount else None,
            incentive_max_amount=float(p.incentive_max_amount) if p.incentive_max_amount else None,
            incentive_percentage=float(p.incentive_percentage) if p.incentive_percentage else None,
            funding_status=p.funding_status,
            claim_mechanism=p.claim_mechanism,
            confidence_score=p.confidence_score,
            start_date=p.start_date.isoformat(),
            end_date=p.end_date.isoformat() if p.end_date else None,
            source_url=p.source_url,
        )
        for p in unique
    ]

    return IncentiveListResponse(incentives=incentive_responses, total=len(incentive_responses))


@router.get("/market-pricing/{make}/{model}")
async def market_pricing(
    make: str,
    model: str,
    zip_code: Optional[str] = Query(None),
):
    """Get real market pricing for a vehicle from MarketCheck inventory data."""
    client = MarketCheckClient()
    try:
        pricing = client.get_market_pricing(make=make, model=model, zip_code=zip_code)
        return {
            "make": pricing.make,
            "model": pricing.model,
            "total_listings": pricing.total_listings,
            "avg_price": pricing.avg_price,
            "min_price": pricing.min_price,
            "max_price": pricing.max_price,
            "avg_msrp": pricing.avg_msrp,
            "nearby_dealers": [
                {
                    "year": l.year,
                    "trim": l.trim,
                    "price": l.price,
                    "msrp": l.msrp,
                    "dealer_name": l.dealer_name,
                    "dealer_city": l.dealer_city,
                    "dealer_state": l.dealer_state,
                    "listing_url": l.listing_url,
                }
                for l in pricing.sample_listings
            ],
        }
    except Exception as e:
        logger.error("Market pricing error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
