import hashlib
import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.lead import Lead
from app.models.consent_record import ConsentRecord
from app.schemas.leads import (
    LeadSubmissionRequest,
    LeadSubmissionResponse,
    IncentiveSummary,
)
from app.services.incentive_matcher import match_incentives
from app.services.lead_scorer import score_lead
from app.services.lead_router import route_lead, get_zip_coordinates

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("", response_model=LeadSubmissionResponse)
async def submit_lead(
    lead_req: LeadSubmissionRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Submit a new lead with consent data. Scores the lead and stores consent record."""
    # Run incentive matching
    vehicle_dict = lead_req.vehicle_interest.model_dump(exclude_none=True)
    buyer_dict = {
        "income_range": lead_req.income_range,
        "affinity_groups": lead_req.affinity_groups,
        "has_trade_in": lead_req.has_trade_in,
    }

    incentive_result = await match_incentives(
        db=db,
        zip_code=lead_req.zip_code,
        vehicle_interest=vehicle_dict,
        buyer_profile=buyer_dict,
    )

    # Build lead_data dict for scoring
    lead_data = {
        "first_name": lead_req.first_name,
        "last_name": lead_req.last_name,
        "email": lead_req.email,
        "phone": lead_req.phone,
        "zip_code": lead_req.zip_code,
        "full_address": lead_req.full_address,
        "income_range": lead_req.income_range,
        "vehicle_interest": vehicle_dict,
        "purchase_timeline": lead_req.purchase_timeline,
        "has_trade_in": lead_req.has_trade_in,
        "calculator_completed": True,
    }

    score, tier = score_lead(lead_data, incentive_result)

    # Extract matched incentive IDs
    matched_ids = [uuid.UUID(inc["id"]) for inc in incentive_result.get("incentives", [])]

    # Create Lead record
    lead = Lead(
        first_name=lead_req.first_name,
        last_name=lead_req.last_name,
        email=lead_req.email,
        phone=lead_req.phone,
        zip_code=lead_req.zip_code,
        full_address=lead_req.full_address,
        income_range=lead_req.income_range,
        vehicle_interest=vehicle_dict,
        affinity_groups=lead_req.affinity_groups,
        purchase_timeline=lead_req.purchase_timeline,
        has_trade_in=lead_req.has_trade_in,
        score=score,
        tier=tier,
        matched_incentive_ids=matched_ids,
        total_savings_estimate=incentive_result["total_savings"],
        source="web",
        source_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent", "")[:500],
    )
    db.add(lead)
    await db.flush()

    # Create a general consent record (no dealer yet — captured at submission time)
    consent_language_hash = hashlib.sha256(lead_req.consent_text.encode()).hexdigest()
    consent = ConsentRecord(
        lead_id=lead.id,
        dealer_id=None,
        consent_timestamp=datetime.now(timezone.utc),
        consent_ip=request.client.host if request.client else "0.0.0.0",
        consent_user_agent=request.headers.get("user-agent", "")[:500],
        consent_page_url=lead_req.consent_page_url or request.headers.get("referer", ""),
        consent_language_version=consent_language_hash,
        consent_method="web_form",
        trustedform_cert_url=lead_req.trustedform_cert_url,
    )
    db.add(consent)
    await db.commit()

    # --- Route lead to matching dealers ---
    matched_dealer_count = 0
    try:
        lead_coords = await get_zip_coordinates(lead_req.zip_code)
        if lead_coords:
            lead_lat, lead_lon = lead_coords
            delivery_results = await route_lead(
                db=db,
                lead=lead,
                lead_lat=lead_lat,
                lead_lon=lead_lon,
                incentives=incentive_result.get("incentives", []),
                total_savings=incentive_result["total_savings"],
            )
            matched_dealer_count = len(delivery_results)

            # Create per-dealer consent records for TCPA compliance
            now = datetime.now(timezone.utc)
            for dr in delivery_results:
                dealer_consent = ConsentRecord(
                    lead_id=lead.id,
                    dealer_id=uuid.UUID(dr["dealer_id"]),
                    consent_timestamp=now,
                    consent_ip=request.client.host if request.client else "0.0.0.0",
                    consent_user_agent=request.headers.get("user-agent", "")[:500],
                    consent_page_url=lead_req.consent_page_url or request.headers.get("referer", ""),
                    consent_language_version=consent_language_hash,
                    consent_method="web_form",
                    trustedform_cert_url=lead_req.trustedform_cert_url,
                )
                db.add(dealer_consent)
            if delivery_results:
                await db.commit()

            logger.info(
                "Lead %s routed to %d dealer(s): %s",
                lead.id,
                matched_dealer_count,
                [dr["dealer_name"] for dr in delivery_results],
            )
        else:
            logger.warning("Could not geocode ZIP %s for lead %s, skipping routing", lead_req.zip_code, lead.id)
    except Exception as e:
        logger.error("Lead routing failed for lead %s: %s", lead.id, e, exc_info=True)

    incentive_summaries = [
        IncentiveSummary(
            id=inc["id"],
            name=inc["name"],
            type=inc["type"],
            amount=inc["amount"],
        )
        for inc in incentive_result.get("incentives", [])
    ]

    return LeadSubmissionResponse(
        lead_id=str(lead.id),
        score=score,
        tier=tier,
        matched_incentives=incentive_summaries,
        total_savings_estimate=incentive_result["total_savings"],
        matched_dealer_count=matched_dealer_count,
    )
