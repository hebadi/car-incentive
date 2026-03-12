"""Stripe billing service.

Manages dealer subscriptions with tiered pricing:
- Starter: $299/mo base + $40/lead metered
- Growth: $599/mo base + $35/lead metered
- Enterprise: $999/mo base + $30/lead metered
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

STRIPE_API_BASE = "https://api.stripe.com/v1"

TIER_CONFIG = {
    "starter": {
        "name": "Starter",
        "base_price_cents": 29900,
        "per_lead_price_cents": 4000,
        "leads_included": 25,
    },
    "growth": {
        "name": "Growth",
        "base_price_cents": 59900,
        "per_lead_price_cents": 3500,
        "leads_included": 50,
    },
    "enterprise": {
        "name": "Enterprise",
        "base_price_cents": 99900,
        "per_lead_price_cents": 3000,
        "leads_included": 100,
    },
}


def _stripe_headers() -> dict:
    return {
        "Authorization": f"Bearer {settings.stripe_secret_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }


async def _stripe_post(endpoint: str, data: dict) -> dict:
    """Make a POST request to Stripe API."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{STRIPE_API_BASE}/{endpoint}",
            data=data,
            headers=_stripe_headers(),
        )
    resp.raise_for_status()
    return resp.json()


async def _stripe_get(endpoint: str, params: dict | None = None) -> dict:
    """Make a GET request to Stripe API."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{STRIPE_API_BASE}/{endpoint}",
            params=params or {},
            headers=_stripe_headers(),
        )
    resp.raise_for_status()
    return resp.json()


async def create_stripe_customer(dealer_name: str, dealer_email: str, dealer_id: str) -> str:
    """Create a Stripe customer for a dealer. Returns customer ID."""
    result = await _stripe_post("customers", {
        "name": dealer_name,
        "email": dealer_email,
        "metadata[dealer_id]": dealer_id,
    })
    return result["id"]


async def create_checkout_session(
    customer_id: str,
    tier: str,
    success_url: str,
    cancel_url: str,
) -> dict:
    """Create a Stripe Checkout session for a new subscription.

    Returns dict with checkout session id and url.
    """
    config = TIER_CONFIG[tier]

    result = await _stripe_post("checkout/sessions", {
        "customer": customer_id,
        "mode": "subscription",
        "success_url": success_url,
        "cancel_url": cancel_url,
        "line_items[0][price_data][currency]": "usd",
        "line_items[0][price_data][product_data][name]": f"IncentiveDrive {config['name']}",
        "line_items[0][price_data][unit_amount]": str(config["base_price_cents"]),
        "line_items[0][price_data][recurring][interval]": "month",
        "line_items[0][quantity]": "1",
        "subscription_data[metadata][tier]": tier,
    })
    return {"session_id": result["id"], "url": result["url"]}


async def report_lead_usage(subscription_id: str, tier: str, quantity: int = 1) -> dict:
    """Report metered lead delivery as a usage event to Stripe.

    Creates an invoice item for the per-lead charge.
    """
    config = TIER_CONFIG[tier]

    # Get the subscription to find the customer
    sub = await _stripe_get(f"subscriptions/{subscription_id}")
    customer_id = sub["customer"]

    result = await _stripe_post("invoiceitems", {
        "customer": customer_id,
        "amount": str(config["per_lead_price_cents"] * quantity),
        "currency": "usd",
        "description": f"Lead delivery ({quantity} lead{'s' if quantity > 1 else ''}) - {config['name']} tier",
        "subscription": subscription_id,
    })
    return {"invoice_item_id": result["id"]}


async def get_subscription_details(subscription_id: str) -> dict:
    """Get current subscription details from Stripe."""
    sub = await _stripe_get(f"subscriptions/{subscription_id}")
    return {
        "id": sub["id"],
        "status": sub["status"],
        "current_period_start": sub["current_period_start"],
        "current_period_end": sub["current_period_end"],
        "tier": sub.get("metadata", {}).get("tier", "starter"),
        "cancel_at_period_end": sub.get("cancel_at_period_end", False),
    }


async def get_upcoming_invoice(customer_id: str) -> dict:
    """Get upcoming invoice for a customer."""
    invoice = await _stripe_get("invoices/upcoming", {"customer": customer_id})
    return {
        "amount_due": invoice["amount_due"],
        "currency": invoice["currency"],
        "period_start": invoice["period_start"],
        "period_end": invoice["period_end"],
        "lines": [
            {
                "description": line["description"],
                "amount": line["amount"],
            }
            for line in invoice.get("lines", {}).get("data", [])
        ],
    }


async def list_invoices(customer_id: str, limit: int = 12) -> list[dict]:
    """List past invoices for a customer."""
    result = await _stripe_get("invoices", {"customer": customer_id, "limit": str(limit)})
    return [
        {
            "id": inv["id"],
            "number": inv.get("number"),
            "amount_paid": inv["amount_paid"],
            "status": inv["status"],
            "period_start": inv["period_start"],
            "period_end": inv["period_end"],
            "created": inv["created"],
            "hosted_invoice_url": inv.get("hosted_invoice_url"),
            "invoice_pdf": inv.get("invoice_pdf"),
        }
        for inv in result.get("data", [])
    ]


async def create_billing_portal_session(customer_id: str, return_url: str) -> str:
    """Create a Stripe Billing Portal session for self-service management.

    Returns the portal URL.
    """
    result = await _stripe_post("billing_portal/sessions", {
        "customer": customer_id,
        "return_url": return_url,
    })
    return result["url"]


def handle_webhook_event(event_type: str, event_data: dict) -> dict:
    """Process Stripe webhook events. Returns action dict.

    Handled events:
    - checkout.session.completed: Activate subscription
    - invoice.paid: Mark payment successful
    - invoice.payment_failed: Flag payment issue
    - customer.subscription.updated: Sync tier/status changes
    - customer.subscription.deleted: Deactivate dealer
    """
    actions = {
        "event_type": event_type,
        "action": "none",
        "dealer_updates": {},
    }

    if event_type == "checkout.session.completed":
        session = event_data.get("object", {})
        actions["action"] = "activate_subscription"
        actions["dealer_updates"] = {
            "stripe_customer_id": session.get("customer"),
            "stripe_subscription_id": session.get("subscription"),
            "is_active": True,
        }

    elif event_type == "invoice.paid":
        actions["action"] = "payment_success"

    elif event_type == "invoice.payment_failed":
        actions["action"] = "payment_failed"
        actions["dealer_updates"] = {
            "payment_issue": True,
        }

    elif event_type == "customer.subscription.updated":
        sub = event_data.get("object", {})
        tier = sub.get("metadata", {}).get("tier", "starter")
        actions["action"] = "subscription_updated"
        actions["dealer_updates"] = {
            "subscription_tier": tier,
            "is_active": sub.get("status") == "active",
        }

    elif event_type == "customer.subscription.deleted":
        actions["action"] = "subscription_cancelled"
        actions["dealer_updates"] = {
            "is_active": False,
            "stripe_subscription_id": None,
        }

    return actions
