import math
import uuid

from fastapi import APIRouter, Depends, Path, Query, Header, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.dealer import Dealer
from app.models.lead import Lead
from app.models.lead_dealer_match import LeadDealerMatch
from app.schemas.dealers import DealerSummary, DealerSearchResponse
from app.schemas.leads import DealerLeadResponse, DealerLeadListResponse, DealerAnalyticsResponse
from app.services.incentive_matcher import zip_to_state

router = APIRouter()

# Approximate ZIP code centroids for distance calculation (MVP).
# In production, use a geocoding service or PostGIS.
_ZIP_APPROX_COORDS: dict[str, tuple[float, float]] = {}


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in miles between two lat/lon points."""
    R = 3959  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


@router.get("/{zip_code}", response_model=DealerSearchResponse)
async def find_dealers_by_zip(
    zip_code: str = Path(..., min_length=5, max_length=10, pattern=r"^\d{5}(-\d{4})?$"),
    radius: int = Query(25, ge=5, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Find dealers within radius of a ZIP code."""
    state = zip_to_state(zip_code)
    if not state:
        return DealerSearchResponse(dealers=[], total=0)

    # Query dealers in the same state (MVP approximation; PostGIS for production)
    stmt = select(Dealer).where(
        Dealer.is_active.is_(True),
        Dealer.state == state,
    )
    result = await db.execute(stmt)
    dealers = result.scalars().all()

    # For MVP, return all dealers in the state with a placeholder distance
    dealer_summaries = [
        DealerSummary(
            id=str(d.id),
            name=d.name,
            phone=d.phone,
            address=d.address,
            city=d.city,
            state=d.state,
            zip_code=d.zip_code,
            makes=d.makes or [],
            distance_miles=None,  # Would need geocoding to compute
        )
        for d in dealers
    ]

    return DealerSearchResponse(dealers=dealer_summaries, total=len(dealer_summaries))


@router.get("/dealer/leads", response_model=DealerLeadListResponse)
async def get_dealer_leads(
    x_dealer_id: str = Header(..., alias="X-Dealer-ID"),
    db: AsyncSession = Depends(get_db),
):
    """Dealer-facing: list leads assigned to the authenticated dealer."""
    try:
        dealer_id = uuid.UUID(x_dealer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid dealer ID format")

    # Verify dealer exists
    dealer_result = await db.execute(
        select(Dealer).where(Dealer.id == dealer_id, Dealer.is_active.is_(True))
    )
    dealer = dealer_result.scalar_one_or_none()
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer not found")

    # Get matched leads
    stmt = (
        select(Lead, LeadDealerMatch)
        .join(LeadDealerMatch, Lead.id == LeadDealerMatch.lead_id)
        .where(LeadDealerMatch.dealer_id == dealer_id)
        .order_by(Lead.created_at.desc())
        .limit(100)
    )
    result = await db.execute(stmt)
    rows = result.all()

    leads = [
        DealerLeadResponse(
            lead_id=str(lead.id),
            first_name=lead.first_name,
            last_name=lead.last_name,
            email=lead.email,
            phone=lead.phone,
            zip_code=lead.zip_code,
            score=lead.score,
            tier=lead.tier,
            total_savings_estimate=float(lead.total_savings_estimate),
            vehicle_interest=lead.vehicle_interest or {},
            created_at=lead.created_at.isoformat(),
        )
        for lead, match in rows
    ]

    return DealerLeadListResponse(leads=leads, total=len(leads))


@router.get("/dealer/analytics", response_model=DealerAnalyticsResponse)
async def get_dealer_analytics(
    x_dealer_id: str = Header(..., alias="X-Dealer-ID"),
    db: AsyncSession = Depends(get_db),
):
    """Dealer-facing: lead count, score distribution, response metrics."""
    try:
        dealer_id = uuid.UUID(x_dealer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid dealer ID format")

    # Verify dealer exists
    dealer_result = await db.execute(
        select(Dealer).where(Dealer.id == dealer_id, Dealer.is_active.is_(True))
    )
    dealer = dealer_result.scalar_one_or_none()
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer not found")

    # Aggregate lead stats
    stmt = (
        select(
            func.count(Lead.id).label("total"),
            func.count(Lead.id).filter(Lead.tier == "hot").label("hot"),
            func.count(Lead.id).filter(Lead.tier == "warm").label("warm"),
            func.count(Lead.id).filter(Lead.tier == "nurture").label("nurture"),
            func.avg(Lead.score).label("avg_score"),
        )
        .join(LeadDealerMatch, Lead.id == LeadDealerMatch.lead_id)
        .where(LeadDealerMatch.dealer_id == dealer_id)
    )
    result = await db.execute(stmt)
    row = result.one()

    return DealerAnalyticsResponse(
        total_leads=row.total or 0,
        hot_leads=row.hot or 0,
        warm_leads=row.warm or 0,
        nurture_leads=row.nurture or 0,
        avg_score=round(float(row.avg_score or 0), 1),
        avg_response_time_minutes=None,  # Requires delivery tracking data
    )
