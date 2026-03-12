"""Admin routes for dealer and lead management, data refresh."""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.dealer import Dealer
from app.models.lead import Lead
from app.models.lead_delivery import LeadDelivery
from app.services.marketcheck_client import MarketCheckClient

logger = logging.getLogger(__name__)

router = APIRouter()


class CreateDealerRequest(BaseModel):
    name: str
    contact_email: str
    crm_email: str | None = None
    phone: str
    address: str
    city: str
    state: str
    zip_code: str
    latitude: float
    longitude: float
    makes: list[str] = []
    subscription_tier: str = "starter"
    max_leads_per_day: int = 50
    min_lead_score: int = 20
    radius_miles: int = 25
    exclusive_leads: bool = False


class UpdateDealerRequest(BaseModel):
    name: str | None = None
    contact_email: str | None = None
    crm_email: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    makes: list[str] | None = None
    subscription_tier: str | None = None
    max_leads_per_day: int | None = None
    min_lead_score: int | None = None
    radius_miles: int | None = None
    exclusive_leads: bool | None = None
    is_active: bool | None = None


@router.post("/dealers")
async def create_dealer(req: CreateDealerRequest, db: AsyncSession = Depends(get_db)):
    """Create a new dealer (manual onboarding for MVP)."""
    dealer = Dealer(
        name=req.name,
        contact_email=req.contact_email,
        crm_email=req.crm_email,
        phone=req.phone,
        address=req.address,
        city=req.city,
        state=req.state,
        zip_code=req.zip_code,
        latitude=req.latitude,
        longitude=req.longitude,
        makes=req.makes,
        subscription_tier=req.subscription_tier,
        max_leads_per_day=req.max_leads_per_day,
        min_lead_score=req.min_lead_score,
        radius_miles=req.radius_miles,
        exclusive_leads=req.exclusive_leads,
    )
    db.add(dealer)
    await db.commit()
    await db.refresh(dealer)

    return {
        "id": str(dealer.id),
        "name": dealer.name,
        "contact_email": dealer.contact_email,
        "state": dealer.state,
        "subscription_tier": dealer.subscription_tier,
        "is_active": dealer.is_active,
        "created_at": dealer.created_at.isoformat() if dealer.created_at else None,
    }


@router.put("/dealers/{dealer_id}")
async def update_dealer(
    dealer_id: str, req: UpdateDealerRequest, db: AsyncSession = Depends(get_db)
):
    """Update dealer settings."""
    result = await db.execute(select(Dealer).where(Dealer.id == dealer_id))
    dealer = result.scalar_one_or_none()
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer not found")

    update_data = req.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(dealer, field, value)

    dealer.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(dealer)

    return {
        "id": str(dealer.id),
        "name": dealer.name,
        "contact_email": dealer.contact_email,
        "subscription_tier": dealer.subscription_tier,
        "is_active": dealer.is_active,
        "updated_at": dealer.updated_at.isoformat() if dealer.updated_at else None,
    }


@router.get("/dealers")
async def list_dealers(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    active_only: bool = Query(False),
):
    """List all dealers with subscription status."""
    query = select(Dealer).offset(skip).limit(limit).order_by(Dealer.created_at.desc())
    if active_only:
        query = query.where(Dealer.is_active == True)  # noqa: E712

    result = await db.execute(query)
    dealers = result.scalars().all()

    count_result = await db.execute(select(func.count(Dealer.id)))
    total = count_result.scalar() or 0

    return {
        "dealers": [
            {
                "id": str(d.id),
                "name": d.name,
                "contact_email": d.contact_email,
                "city": d.city,
                "state": d.state,
                "makes": d.makes or [],
                "subscription_tier": d.subscription_tier,
                "is_active": d.is_active,
                "max_leads_per_day": d.max_leads_per_day,
                "min_lead_score": d.min_lead_score,
                "radius_miles": d.radius_miles,
                "created_at": d.created_at.isoformat() if d.created_at else None,
            }
            for d in dealers
        ],
        "total": total,
    }


@router.get("/leads")
async def list_all_leads(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    tier: str | None = Query(None),
):
    """List all leads with delivery status."""
    query = select(Lead).offset(skip).limit(limit).order_by(Lead.created_at.desc())
    if tier:
        query = query.where(Lead.tier == tier)

    result = await db.execute(query)
    leads = result.scalars().all()

    count_result = await db.execute(select(func.count(Lead.id)))
    total = count_result.scalar() or 0

    # Fetch delivery status for each lead
    lead_data = []
    for lead in leads:
        delivery_result = await db.execute(
            select(LeadDelivery).where(LeadDelivery.lead_id == lead.id)
        )
        deliveries = delivery_result.scalars().all()

        lead_data.append({
            "id": str(lead.id),
            "name": f"{lead.first_name} {lead.last_name}",
            "email": lead.email,
            "zip_code": lead.zip_code,
            "score": lead.score,
            "tier": lead.tier,
            "total_savings": float(lead.total_savings_estimate or 0),
            "vehicle_interest": lead.vehicle_interest or {},
            "deliveries": [
                {
                    "dealer_id": str(d.dealer_id),
                    "status": d.status,
                    "method": d.delivery_method,
                    "sent_at": d.sent_at.isoformat() if d.sent_at else None,
                }
                for d in deliveries
            ],
            "created_at": lead.created_at.isoformat() if lead.created_at else None,
        })

    return {"leads": lead_data, "total": total}


# ---- Incentive Data Management ----


@router.post("/refresh-incentives")
async def trigger_refresh():
    """Trigger an incentive data refresh from all sources (scrapers + MarketCheck API).

    In production, schedule this via cron or Celery beat (daily/weekly).
    """
    from app.tasks.refresh_incentives import _refresh_async

    try:
        result = await _refresh_async()
        return result
    except Exception as e:
        logger.error("Refresh failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Refresh failed: {str(e)}")


@router.get("/marketcheck-status")
async def marketcheck_status():
    """Check MarketCheck API connectivity and mode."""
    client = MarketCheckClient()
    return {
        "mock_mode": client.is_mock,
        "api_key_configured": bool(settings.marketcheck_api_key),
        "monitored_makes": [
            "Hyundai", "Kia", "Toyota", "Honda", "Ford",
            "Chevrolet", "Nissan", "Volkswagen", "Tesla", "Ram", "Dodge",
        ],
    }


@router.get("/marketcheck-preview/{make}")
async def preview_incentives(make: str):
    """Preview what MarketCheck returns for a given make (uses mock data if no API key)."""
    client = MarketCheckClient()
    incentives = client.get_oem_incentives(make)
    return {
        "make": make,
        "mock_mode": client.is_mock,
        "count": len(incentives),
        "incentives": [
            {
                "name": inc.name,
                "model": inc.model,
                "type": inc.incentive_type,
                "amount": inc.amount,
                "percentage": inc.percentage,
                "start_date": inc.start_date,
                "end_date": inc.end_date,
                "description": inc.description,
            }
            for inc in incentives
        ],
    }


@router.get("/market-pricing/{make}/{model}")
async def market_pricing(
    make: str,
    model: str,
    zip_code: Optional[str] = Query(None),
    inventory_type: str = Query("new"),
):
    """Get real market pricing for a make/model from MarketCheck vehicle listings."""
    client = MarketCheckClient()
    try:
        pricing = client.get_market_pricing(
            make=make,
            model=model,
            zip_code=zip_code,
            inventory_type=inventory_type,
        )
        return {
            "make": pricing.make,
            "model": pricing.model,
            "mock_mode": client.is_mock,
            "total_listings": pricing.total_listings,
            "avg_price": pricing.avg_price,
            "min_price": pricing.min_price,
            "max_price": pricing.max_price,
            "avg_msrp": pricing.avg_msrp,
            "sample_listings": [
                {
                    "year": l.year,
                    "trim": l.trim,
                    "price": l.price,
                    "msrp": l.msrp,
                    "dealer_name": l.dealer_name,
                    "dealer_city": l.dealer_city,
                    "dealer_state": l.dealer_state,
                    "listing_url": l.listing_url,
                    "photo_url": l.photo_url,
                }
                for l in pricing.sample_listings
            ],
        }
    except Exception as e:
        logger.error("Market pricing error for %s %s: %s", make, model, e)
        raise HTTPException(status_code=500, detail=f"Market pricing error: {str(e)}")
