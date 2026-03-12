"""Dealer portal API routes.

Provides endpoints for authenticated dealers to manage leads, view stats,
and update settings.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.dealer import Dealer
from app.models.lead import Lead
from app.models.lead_delivery import LeadDelivery
from app.models.lead_dealer_match import LeadDealerMatch
from app.models.consent_record import ConsentRecord
from app.models.incentive_program import IncentiveProgram

router = APIRouter()


class DealerSettingsUpdate(BaseModel):
    crm_email: str | None = None
    radius_miles: int | None = None
    makes: list[str] | None = None
    max_leads_per_day: int | None = None
    min_lead_score: int | None = None


class LeadNoteUpdate(BaseModel):
    notes: str
    status: str | None = None  # new, contacted, converted


@router.get("/dashboard/{dealer_id}")
async def get_dashboard(dealer_id: str, db: AsyncSession = Depends(get_db)):
    """Get dealer dashboard stats."""
    result = await db.execute(select(Dealer).where(Dealer.id == dealer_id))
    dealer = result.scalar_one_or_none()
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer not found")

    # Time ranges
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Total leads this month
    total_leads_result = await db.execute(
        select(func.count(LeadDelivery.id))
        .where(LeadDelivery.dealer_id == dealer.id)
        .where(LeadDelivery.created_at >= month_start)
        .where(LeadDelivery.status.in_(["sent", "delivered"]))
    )
    total_leads = total_leads_result.scalar() or 0

    # Get lead IDs delivered to this dealer this month
    lead_ids_result = await db.execute(
        select(LeadDelivery.lead_id)
        .where(LeadDelivery.dealer_id == dealer.id)
        .where(LeadDelivery.created_at >= month_start)
        .where(LeadDelivery.status.in_(["sent", "delivered"]))
    )
    lead_ids = [r[0] for r in lead_ids_result.fetchall()]

    # Average lead score
    avg_score = 0
    tier_counts = {"hot": 0, "warm": 0, "nurture": 0}
    if lead_ids:
        score_result = await db.execute(
            select(func.avg(Lead.score)).where(Lead.id.in_(lead_ids))
        )
        avg_score = round(score_result.scalar() or 0, 1)

        # Leads by tier
        for tier_name in tier_counts:
            tier_result = await db.execute(
                select(func.count(Lead.id))
                .where(Lead.id.in_(lead_ids))
                .where(Lead.tier == tier_name)
            )
            tier_counts[tier_name] = tier_result.scalar() or 0

    return {
        "dealer_name": dealer.name,
        "subscription_tier": dealer.subscription_tier,
        "total_leads_this_month": total_leads,
        "avg_lead_score": avg_score,
        "leads_by_tier": tier_counts,
        "max_leads_per_day": dealer.max_leads_per_day,
        "radius_miles": dealer.radius_miles,
    }


@router.get("/leads/{dealer_id}")
async def get_dealer_leads(
    dealer_id: str,
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    tier: str | None = Query(None),
    status: str | None = Query(None),
    sort_by: str = Query("date", regex="^(date|score)$"),
):
    """Get leads for a specific dealer with filtering and sorting."""
    # Get lead IDs delivered to this dealer
    delivery_query = (
        select(LeadDelivery.lead_id, LeadDelivery.status, LeadDelivery.sent_at)
        .where(LeadDelivery.dealer_id == dealer_id)
        .where(LeadDelivery.status.in_(["sent", "delivered"]))
    )
    delivery_result = await db.execute(delivery_query)
    deliveries = {r[0]: {"delivery_status": r[1], "sent_at": r[2]} for r in delivery_result.fetchall()}

    if not deliveries:
        return {"leads": [], "total": 0}

    lead_query = select(Lead).where(Lead.id.in_(deliveries.keys()))
    if tier:
        lead_query = lead_query.where(Lead.tier == tier)

    if sort_by == "score":
        lead_query = lead_query.order_by(Lead.score.desc())
    else:
        lead_query = lead_query.order_by(Lead.created_at.desc())

    lead_query = lead_query.offset(skip).limit(limit)
    result = await db.execute(lead_query)
    leads = result.scalars().all()

    count_query = select(func.count(Lead.id)).where(Lead.id.in_(deliveries.keys()))
    if tier:
        count_query = count_query.where(Lead.tier == tier)
    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    return {
        "leads": [
            {
                "id": str(lead.id),
                "first_name": lead.first_name,
                "last_name": lead.last_name,
                "email": lead.email,
                "phone": lead.phone,
                "zip_code": lead.zip_code,
                "vehicle_interest": lead.vehicle_interest or {},
                "score": lead.score,
                "tier": lead.tier,
                "total_savings": float(lead.total_savings_estimate or 0),
                "delivery_status": deliveries.get(lead.id, {}).get("delivery_status"),
                "sent_at": deliveries.get(lead.id, {}).get("sent_at", ""),
                "created_at": lead.created_at.isoformat() if lead.created_at else None,
            }
            for lead in leads
        ],
        "total": total,
    }


@router.get("/leads/{dealer_id}/{lead_id}")
async def get_lead_detail(dealer_id: str, lead_id: str, db: AsyncSession = Depends(get_db)):
    """Get full lead detail including incentive breakdown and delivery status."""
    # Verify this lead was delivered to this dealer
    delivery_result = await db.execute(
        select(LeadDelivery)
        .where(LeadDelivery.dealer_id == dealer_id)
        .where(LeadDelivery.lead_id == lead_id)
    )
    delivery = delivery_result.scalar_one_or_none()
    if not delivery:
        raise HTTPException(status_code=404, detail="Lead not found for this dealer")

    lead_result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = lead_result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # Get incentive details
    incentive_details = []
    if lead.matched_incentive_ids:
        for inc_id in lead.matched_incentive_ids:
            inc_result = await db.execute(
                select(IncentiveProgram).where(IncentiveProgram.id == inc_id)
            )
            inc = inc_result.scalar_one_or_none()
            if inc:
                incentive_details.append({
                    "id": str(inc.id),
                    "name": inc.name,
                    "type": inc.type,
                    "amount": float(inc.incentive_amount or 0),
                    "claim_mechanism": inc.claim_mechanism,
                })

    # Get consent record
    consent_result = await db.execute(
        select(ConsentRecord)
        .where(ConsentRecord.lead_id == lead_id)
        .where(ConsentRecord.dealer_id == dealer_id)
    )
    consent = consent_result.scalar_one_or_none()

    return {
        "id": str(lead.id),
        "first_name": lead.first_name,
        "last_name": lead.last_name,
        "email": lead.email,
        "phone": lead.phone,
        "zip_code": lead.zip_code,
        "full_address": lead.full_address,
        "income_range": lead.income_range,
        "vehicle_interest": lead.vehicle_interest or {},
        "affinity_groups": lead.affinity_groups or [],
        "purchase_timeline": lead.purchase_timeline,
        "has_trade_in": lead.has_trade_in,
        "score": lead.score,
        "tier": lead.tier,
        "total_savings": float(lead.total_savings_estimate or 0),
        "incentives": incentive_details,
        "delivery": {
            "status": delivery.status,
            "method": delivery.delivery_method,
            "sent_at": delivery.sent_at.isoformat() if delivery.sent_at else None,
            "error": delivery.error_message,
        },
        "consent": {
            "timestamp": consent.consent_timestamp.isoformat() if consent else None,
            "method": consent.consent_method if consent else None,
            "revoked": consent.revoked if consent else None,
        } if consent else None,
        "created_at": lead.created_at.isoformat() if lead.created_at else None,
    }


@router.get("/settings/{dealer_id}")
async def get_dealer_settings(dealer_id: str, db: AsyncSession = Depends(get_db)):
    """Get dealer settings."""
    result = await db.execute(select(Dealer).where(Dealer.id == dealer_id))
    dealer = result.scalar_one_or_none()
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer not found")

    return {
        "id": str(dealer.id),
        "name": dealer.name,
        "contact_email": dealer.contact_email,
        "crm_email": dealer.crm_email,
        "phone": dealer.phone,
        "address": dealer.address,
        "city": dealer.city,
        "state": dealer.state,
        "zip_code": dealer.zip_code,
        "makes": dealer.makes or [],
        "subscription_tier": dealer.subscription_tier,
        "max_leads_per_day": dealer.max_leads_per_day,
        "min_lead_score": dealer.min_lead_score,
        "radius_miles": dealer.radius_miles,
        "exclusive_leads": dealer.exclusive_leads,
    }


@router.put("/settings/{dealer_id}")
async def update_dealer_settings(
    dealer_id: str, req: DealerSettingsUpdate, db: AsyncSession = Depends(get_db)
):
    """Update dealer settings (self-service from portal)."""
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

    return {"status": "ok", "updated_fields": list(update_data.keys())}
