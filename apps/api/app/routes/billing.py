"""Billing routes for Stripe subscription management."""

import hashlib
import hmac
import json
import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.dealer import Dealer
from app.services.billing import (
    create_checkout_session,
    create_billing_portal_session,
    create_stripe_customer,
    get_subscription_details,
    get_upcoming_invoice,
    handle_webhook_event,
    list_invoices,
    TIER_CONFIG,
)

logger = logging.getLogger(__name__)
router = APIRouter()


class CheckoutRequest(BaseModel):
    dealer_id: str
    tier: str
    success_url: str = "http://localhost:3001/billing?success=true"
    cancel_url: str = "http://localhost:3001/billing?canceled=true"


class PortalRequest(BaseModel):
    dealer_id: str
    return_url: str = "http://localhost:3001/billing"


@router.get("/tiers")
async def get_pricing_tiers():
    """Get available pricing tiers."""
    return {
        tier_key: {
            "name": config["name"],
            "base_price": config["base_price_cents"] / 100,
            "per_lead_price": config["per_lead_price_cents"] / 100,
            "leads_included": config["leads_included"],
        }
        for tier_key, config in TIER_CONFIG.items()
    }


@router.post("/checkout")
async def create_checkout(req: CheckoutRequest, db: AsyncSession = Depends(get_db)):
    """Create a Stripe Checkout session for a dealer subscription."""
    if req.tier not in TIER_CONFIG:
        raise HTTPException(status_code=400, detail=f"Invalid tier: {req.tier}")

    result = await db.execute(select(Dealer).where(Dealer.id == req.dealer_id))
    dealer = result.scalar_one_or_none()
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer not found")

    # Create Stripe customer if needed
    if not dealer.stripe_customer_id:
        customer_id = await create_stripe_customer(
            dealer.name, dealer.contact_email, str(dealer.id)
        )
        dealer.stripe_customer_id = customer_id
        await db.commit()
    else:
        customer_id = dealer.stripe_customer_id

    session = await create_checkout_session(
        customer_id=customer_id,
        tier=req.tier,
        success_url=req.success_url,
        cancel_url=req.cancel_url,
    )
    return session


@router.post("/portal")
async def create_portal(req: PortalRequest, db: AsyncSession = Depends(get_db)):
    """Create a Stripe Billing Portal session for self-service management."""
    result = await db.execute(select(Dealer).where(Dealer.id == req.dealer_id))
    dealer = result.scalar_one_or_none()
    if not dealer or not dealer.stripe_customer_id:
        raise HTTPException(status_code=404, detail="Dealer or Stripe customer not found")

    url = await create_billing_portal_session(dealer.stripe_customer_id, req.return_url)
    return {"url": url}


@router.get("/subscription/{dealer_id}")
async def get_dealer_subscription(dealer_id: str, db: AsyncSession = Depends(get_db)):
    """Get subscription details for a dealer."""
    result = await db.execute(select(Dealer).where(Dealer.id == dealer_id))
    dealer = result.scalar_one_or_none()
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer not found")

    if not dealer.stripe_subscription_id:
        return {
            "has_subscription": False,
            "tier": dealer.subscription_tier,
        }

    sub = await get_subscription_details(dealer.stripe_subscription_id)
    return {"has_subscription": True, **sub}


@router.get("/invoices/{dealer_id}")
async def get_dealer_invoices(dealer_id: str, db: AsyncSession = Depends(get_db)):
    """Get invoices for a dealer."""
    result = await db.execute(select(Dealer).where(Dealer.id == dealer_id))
    dealer = result.scalar_one_or_none()
    if not dealer or not dealer.stripe_customer_id:
        raise HTTPException(status_code=404, detail="Dealer or Stripe customer not found")

    invoices = await list_invoices(dealer.stripe_customer_id)
    return {"invoices": invoices}


@router.get("/upcoming/{dealer_id}")
async def get_dealer_upcoming_invoice(dealer_id: str, db: AsyncSession = Depends(get_db)):
    """Get upcoming invoice for a dealer."""
    result = await db.execute(select(Dealer).where(Dealer.id == dealer_id))
    dealer = result.scalar_one_or_none()
    if not dealer or not dealer.stripe_customer_id:
        raise HTTPException(status_code=404, detail="Dealer or Stripe customer not found")

    invoice = await get_upcoming_invoice(dealer.stripe_customer_id)
    return invoice


@router.post("/webhook")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Handle Stripe webhook events."""
    body = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    # Verify webhook signature
    if settings.stripe_webhook_secret:
        try:
            _verify_stripe_signature(body, sig_header, settings.stripe_webhook_secret)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    event = json.loads(body)
    event_type = event.get("type", "")
    event_data = event.get("data", {})

    actions = handle_webhook_event(event_type, event_data)
    logger.info("Stripe webhook: %s -> %s", event_type, actions["action"])

    # Apply dealer updates
    if actions["dealer_updates"] and actions["action"] != "none":
        customer_id = event_data.get("object", {}).get("customer")
        if customer_id:
            result = await db.execute(
                select(Dealer).where(Dealer.stripe_customer_id == customer_id)
            )
            dealer = result.scalar_one_or_none()
            if dealer:
                updates = actions["dealer_updates"]
                if "stripe_subscription_id" in updates:
                    dealer.stripe_subscription_id = updates["stripe_subscription_id"]
                if "subscription_tier" in updates:
                    dealer.subscription_tier = updates["subscription_tier"]
                if "is_active" in updates:
                    dealer.is_active = updates["is_active"]
                if "stripe_customer_id" in updates:
                    dealer.stripe_customer_id = updates["stripe_customer_id"]
                await db.commit()

    return {"status": "ok"}


def _verify_stripe_signature(payload: bytes, sig_header: str, secret: str) -> None:
    """Verify Stripe webhook signature."""
    elements = dict(item.split("=", 1) for item in sig_header.split(",") if "=" in item)
    timestamp = elements.get("t", "")
    signature = elements.get("v1", "")

    if not timestamp or not signature:
        raise ValueError("Invalid signature header")

    signed_payload = f"{timestamp}.{payload.decode('utf-8')}"
    expected = hmac.new(
        secret.encode("utf-8"),
        signed_payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        raise ValueError("Signature verification failed")
