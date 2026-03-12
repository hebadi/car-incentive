"""ADF XML lead delivery service.

Generates ADF 1.0 XML and delivers via SMTP (SendGrid).
Includes retry logic with exponential backoff.
"""
from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime, timezone
from xml.sax.saxutils import escape as xml_escape

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

SENDGRID_API_URL = "https://api.sendgrid.com/v3/mail/send"
MAX_RETRIES = 3
BACKOFF_BASE = 4  # 1s, 4s, 16s


def generate_adf_xml(
    lead: dict,
    dealer: dict,
    incentives: list[dict],
    total_savings: float,
    lead_score: int,
) -> str:
    """Generate ADF 1.0 XML for lead delivery.

    Args:
        lead: Lead data dict with keys: first_name, last_name, email, phone,
              vehicle_interest (dict with year, make, model, trim).
        dealer: Dealer data dict with keys: name.
        incentives: List of incentive dicts with keys: name, amount.
        total_savings: Total savings estimate.
        lead_score: Numeric lead score (0-100).
    """
    vehicle = lead.get("vehicle_interest", {})
    request_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
    # Format timezone as -05:00 instead of -0500
    request_date = request_date[:-2] + ":" + request_date[-2:]

    incentive_lines = []
    for inc in incentives:
        incentive_lines.append(
            f"        {xml_escape(inc.get('name', 'Unknown'))}: ${inc.get('amount', 0):,.2f}"
        )
    incentive_text = "\n".join(incentive_lines) if incentive_lines else "        No specific incentives matched."

    comments = (
        f"Qualified incentives:\n{incentive_text}\n"
        f"        Total estimated savings: ${total_savings:,.2f}.\n"
        f"        Lead Score: {lead_score} ({'Hot' if lead_score >= 80 else 'Warm' if lead_score >= 50 else 'Nurture'})."
        f" Source: IncentiveDrive."
    )

    phone_element = ""
    if lead.get("phone"):
        phone_element = f'\n        <phone type="cellphone">{xml_escape(lead["phone"])}</phone>'

    trim_element = ""
    if vehicle.get("trim"):
        trim_element = f"\n      <trim>{xml_escape(vehicle['trim'])}</trim>"

    year_element = f"\n      <year>{xml_escape(str(vehicle.get('year', '')))}</year>" if vehicle.get("year") else ""
    make_element = f"\n      <make>{xml_escape(vehicle.get('make', ''))}</make>" if vehicle.get("make") else ""
    model_element = f"\n      <model>{xml_escape(vehicle.get('model', ''))}</model>" if vehicle.get("model") else ""

    vehicle_status = vehicle.get("new_or_used", "new")
    vehicle_interest = "buy"

    xml = f"""<?ADF VERSION "1.0"?>
<?XML VERSION "1.0"?>
<adf>
  <prospect status="new">
    <requestdate>{request_date}</requestdate>
    <vehicle interest="{xml_escape(vehicle_interest)}" status="{xml_escape(vehicle_status)}">{year_element}{make_element}{model_element}{trim_element}
    </vehicle>
    <customer>
      <contact>
        <name part="first">{xml_escape(lead.get('first_name', ''))}</name>
        <name part="last">{xml_escape(lead.get('last_name', ''))}</name>
        <email>{xml_escape(lead.get('email', ''))}</email>{phone_element}
      </contact>
      <comments>
        {comments}
      </comments>
    </customer>
    <vendor>
      <contact>
        <name part="full">{xml_escape(dealer.get('name', ''))}</name>
      </contact>
    </vendor>
    <provider>
      <name part="full">IncentiveDrive</name>
      <url>https://www.incentivedrive.com</url>
    </provider>
  </prospect>
</adf>"""
    return xml


async def send_adf_email(
    to_email: str,
    adf_xml: str,
    lead_name: str,
    subject: str | None = None,
) -> dict:
    """Send ADF XML via SendGrid SMTP API.

    Returns dict with keys: success (bool), message_id (str|None), error (str|None).
    """
    if not subject:
        subject = f"New Lead from IncentiveDrive: {lead_name}"

    payload = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": "leads@incentivedrive.com", "name": "IncentiveDrive"},
        "subject": subject,
        "content": [
            {"type": "text/xml", "value": adf_xml},
            {"type": "text/plain", "value": f"ADF lead attached for {lead_name}. View in your CRM."},
        ],
    }

    headers = {
        "Authorization": f"Bearer {settings.sendgrid_api_key}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(SENDGRID_API_URL, json=payload, headers=headers)

    if resp.status_code in (200, 201, 202):
        message_id = resp.headers.get("X-Message-Id", str(uuid.uuid4()))
        return {"success": True, "message_id": message_id, "error": None}
    else:
        return {"success": False, "message_id": None, "error": f"SendGrid {resp.status_code}: {resp.text}"}


async def deliver_lead_adf(
    lead: dict,
    dealer: dict,
    incentives: list[dict],
    total_savings: float,
    lead_score: int,
) -> dict:
    """Generate ADF XML and deliver via email with retry logic.

    Returns dict with keys:
        adf_xml, status ('sent' | 'failed'), error, retry_count, sent_at.
    """
    adf_xml = generate_adf_xml(lead, dealer, incentives, total_savings, lead_score)

    to_email = dealer.get("crm_email") or dealer.get("contact_email")
    if not to_email:
        return {
            "adf_xml": adf_xml,
            "status": "failed",
            "error": "No delivery email configured for dealer",
            "retry_count": 0,
            "sent_at": None,
        }

    lead_name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()

    # If SendGrid isn't configured, log the ADF XML and mark as sent (dev mode)
    if not settings.sendgrid_api_key:
        logger.info("SendGrid not configured — ADF XML generated for %s -> %s (dev mode)", lead_name, to_email)
        logger.debug("ADF XML:\n%s", adf_xml)
        return {
            "adf_xml": adf_xml,
            "status": "sent",
            "error": None,
            "retry_count": 0,
            "sent_at": datetime.now(timezone.utc),
        }

    last_error = None
    for attempt in range(MAX_RETRIES):
        if attempt > 0:
            wait = BACKOFF_BASE ** attempt  # 1s, 4s, 16s
            logger.info("ADF delivery retry %d, waiting %ds", attempt, wait)
            await asyncio.sleep(wait)

        result = await send_adf_email(to_email, adf_xml, lead_name)
        if result["success"]:
            return {
                "adf_xml": adf_xml,
                "status": "sent",
                "error": None,
                "retry_count": attempt,
                "sent_at": datetime.now(timezone.utc),
            }
        last_error = result["error"]
        logger.warning("ADF delivery attempt %d failed: %s", attempt + 1, last_error)

    return {
        "adf_xml": adf_xml,
        "status": "failed",
        "error": last_error,
        "retry_count": MAX_RETRIES,
        "sent_at": None,
    }
