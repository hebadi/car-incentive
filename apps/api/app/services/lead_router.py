"""Lead routing engine.

Matches leads to dealers by geography, franchise, subscription status,
lead caps, and score thresholds. Supports exclusive and shared distribution.
"""
from __future__ import annotations

import logging
import math
import uuid
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dealer import Dealer
from app.models.lead import Lead
from app.models.lead_dealer_match import LeadDealerMatch
from app.models.lead_delivery import LeadDelivery
from app.services.adf_delivery import deliver_lead_adf

logger = logging.getLogger(__name__)

EARTH_RADIUS_MILES = 3958.8
MAX_DEALERS_SHARED = 3
MAX_DEALERS_EXCLUSIVE = 1
RADIUS_INCREMENT = 25
MAX_RADIUS = 100


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in miles between two lat/lon points using Haversine formula."""
    lat1_r, lon1_r = math.radians(lat1), math.radians(lon1)
    lat2_r, lon2_r = math.radians(lat2), math.radians(lon2)

    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return EARTH_RADIUS_MILES * c


# MVP ZIP-to-coordinate lookup.
# Uses the free zippopotam.us API with local caching.
# In production, replace with a local ZIP database for speed.
ZIP_COORD_CACHE: dict[str, tuple[float, float] | None] = {}


async def get_zip_coordinates(zip_code: str) -> tuple[float, float] | None:
    """Get (lat, lon) for a ZIP code via zippopotam.us API, with caching."""
    zip5 = zip_code[:5]
    if zip5 in ZIP_COORD_CACHE:
        return ZIP_COORD_CACHE[zip5]

    try:
        import httpx
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"https://api.zippopotam.us/us/{zip5}")
            if resp.status_code == 200:
                data = resp.json()
                places = data.get("places", [])
                if places:
                    lat = float(places[0]["latitude"])
                    lon = float(places[0]["longitude"])
                    ZIP_COORD_CACHE[zip5] = (lat, lon)
                    return (lat, lon)
    except Exception as e:
        logger.warning("ZIP geocoding failed for %s: %s", zip5, e)

    ZIP_COORD_CACHE[zip5] = None
    return None


async def get_dealer_leads_today(db: AsyncSession, dealer_id: uuid.UUID) -> int:
    """Count leads delivered to a dealer today."""
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    result = await db.execute(
        select(func.count(LeadDelivery.id))
        .where(LeadDelivery.dealer_id == dealer_id)
        .where(LeadDelivery.created_at >= today_start)
        .where(LeadDelivery.status.in_(["sent", "delivered"]))
    )
    return result.scalar() or 0


async def find_matching_dealers(
    db: AsyncSession,
    lead: Lead,
    lead_lat: float,
    lead_lon: float,
) -> list[dict]:
    """Find dealers matching a lead by geography, franchise, subscription, caps, and score.

    Returns list of dicts sorted by distance, each with keys:
        dealer, distance_miles, match_score.
    """
    result = await db.execute(
        select(Dealer).where(Dealer.is_active == True)  # noqa: E712
    )
    active_dealers = result.scalars().all()

    vehicle_make = None
    if lead.vehicle_interest:
        vehicle_make = lead.vehicle_interest.get("make")

    matches = []
    for dealer in active_dealers:
        # ZIP code radius check
        distance = haversine_distance(lead_lat, lead_lon, dealer.latitude, dealer.longitude)
        if distance > dealer.radius_miles:
            continue

        # Franchise/make filter
        if vehicle_make and dealer.makes:
            if vehicle_make.lower() not in [m.lower() for m in dealer.makes]:
                continue

        # Subscription must be active (is_active already filtered above)

        # Daily lead cap check
        leads_today = await get_dealer_leads_today(db, dealer.id)
        if leads_today >= dealer.max_leads_per_day:
            continue

        # Minimum lead score threshold
        if lead.score < dealer.min_lead_score:
            continue

        # Compute match score: closer distance + higher score preference = better match
        match_score = max(0, 100 - int(distance))
        if vehicle_make and dealer.makes and vehicle_make.lower() in [m.lower() for m in dealer.makes]:
            match_score += 20

        matches.append({
            "dealer": dealer,
            "distance_miles": round(distance, 2),
            "match_score": match_score,
        })

    # Sort by match score descending
    matches.sort(key=lambda m: m["match_score"], reverse=True)
    return matches


async def route_lead(
    db: AsyncSession,
    lead: Lead,
    lead_lat: float,
    lead_lon: float,
    incentives: list[dict],
    total_savings: float,
) -> list[dict]:
    """Main lead routing entry point.

    Finds matching dealers, applies exclusivity rules, triggers ADF delivery.
    Returns list of delivery result dicts.
    """
    # Try finding dealers with expanding radius
    matches = []
    original_radius_dealers = await find_matching_dealers(db, lead, lead_lat, lead_lon)

    if original_radius_dealers:
        matches = original_radius_dealers
    else:
        # Failover: expand radius in 25-mile increments up to 100 miles
        for extra in range(RADIUS_INCREMENT, MAX_RADIUS + 1, RADIUS_INCREMENT):
            # Temporarily relax radius for all dealers
            result = await db.execute(
                select(Dealer).where(Dealer.is_active == True)  # noqa: E712
            )
            all_dealers = result.scalars().all()

            for dealer in all_dealers:
                distance = haversine_distance(lead_lat, lead_lon, dealer.latitude, dealer.longitude)
                expanded_radius = dealer.radius_miles + extra
                if distance > expanded_radius:
                    continue

                vehicle_make = lead.vehicle_interest.get("make") if lead.vehicle_interest else None
                if vehicle_make and dealer.makes:
                    if vehicle_make.lower() not in [m.lower() for m in dealer.makes]:
                        continue

                leads_today = await get_dealer_leads_today(db, dealer.id)
                if leads_today >= dealer.max_leads_per_day:
                    continue

                if lead.score < dealer.min_lead_score:
                    continue

                match_score = max(0, 100 - int(distance))
                matches.append({
                    "dealer": dealer,
                    "distance_miles": round(distance, 2),
                    "match_score": match_score,
                })

            if matches:
                matches.sort(key=lambda m: m["match_score"], reverse=True)
                break

    if not matches:
        logger.info("No matching dealers for lead %s, routing to nurture queue", lead.id)
        return []

    # Determine exclusivity: check if any matched dealer has exclusive_leads enabled
    # Premium tier dealers get exclusive leads
    has_exclusive = any(m["dealer"].exclusive_leads for m in matches)

    if has_exclusive:
        # Route to exactly 1 best-match exclusive dealer
        selected = [matches[0]]
    else:
        # Shared: max 3 dealers
        selected = matches[:MAX_DEALERS_SHARED]

    delivery_results = []
    for match in selected:
        dealer = match["dealer"]
        is_exclusive = has_exclusive and len(selected) == 1

        # Create match record
        lead_match = LeadDealerMatch(
            lead_id=lead.id,
            dealer_id=dealer.id,
            distance_miles=match["distance_miles"],
            match_score=match["match_score"],
            is_exclusive=is_exclusive,
        )
        db.add(lead_match)

        # Prepare lead data for ADF
        lead_data = {
            "first_name": lead.first_name,
            "last_name": lead.last_name,
            "email": lead.email,
            "phone": lead.phone,
            "vehicle_interest": lead.vehicle_interest or {},
        }
        dealer_data = {
            "name": dealer.name,
            "crm_email": dealer.crm_email,
            "contact_email": dealer.contact_email,
        }

        # Deliver ADF
        result = await deliver_lead_adf(
            lead=lead_data,
            dealer=dealer_data,
            incentives=incentives,
            total_savings=total_savings,
            lead_score=lead.score,
        )

        # Create delivery record
        delivery = LeadDelivery(
            lead_id=lead.id,
            dealer_id=dealer.id,
            delivery_method="adf_email",
            status=result["status"],
            adf_xml=result["adf_xml"],
            delivery_email=dealer.crm_email or dealer.contact_email,
            error_message=result.get("error"),
            retry_count=result["retry_count"],
            sent_at=result.get("sent_at"),
        )
        db.add(delivery)

        delivery_results.append({
            "dealer_id": str(dealer.id),
            "dealer_name": dealer.name,
            "status": result["status"],
            "is_exclusive": is_exclusive,
            "distance_miles": match["distance_miles"],
        })

    await db.commit()
    return delivery_results
