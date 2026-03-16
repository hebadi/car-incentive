"""
OEM Incentive Monitor — fetches manufacturer offers pages and uses Claude
to extract structured incentive data, then diffs against the DB.

Runs daily alongside the MarketCheck refresh to catch high-value incentives
that MarketCheck misses (e.g. Hyundai's $10K Dealer Choice Bonus Cash).

Usage (standalone):
    python -m app.tasks.oem_incentive_monitor

Usage (Celery):
    from app.tasks.oem_incentive_monitor import monitor_oem_incentives_task
    monitor_oem_incentives_task.delay()
"""
from __future__ import annotations

import json
import logging
import os
import time
import uuid
from datetime import datetime, timezone

import httpx
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", settings.database_url)

# ---- OEM offers page URLs ----
# Each OEM's public-facing offers/specials page.
# We fetch the HTML content and use Claude to extract incentive data.
OEM_OFFERS_PAGES: dict[str, str] = {
    "Acura": "https://www.acura.com/special-offers",
    "Audi": "https://www.audiusa.com/us/web/en/shopping-tools/special-offers.html",
    "BMW": "https://www.bmwusa.com/byo/build-your-own.html#/offers",
    "Buick": "https://www.buick.com/current-offers",
    "Cadillac": "https://www.cadillac.com/current-offers",
    "Chevrolet": "https://www.chevrolet.com/current-offers",
    "Chrysler": "https://www.chrysler.com/incentives-offers.html",
    "Dodge": "https://www.dodge.com/incentives-offers.html",
    "Ford": "https://www.ford.com/shopping/deal/",
    "Genesis": "https://www.genesis.com/us/en/genesis-special-offers.html",
    "GMC": "https://www.gmc.com/current-offers",
    "Honda": "https://automobiles.honda.com/tools/current-offers",
    "Hyundai": "https://www.hyundaiusa.com/us/en/deals-and-specials",
    "Infiniti": "https://www.infinitiusa.com/shopping-tools/offers-incentives",
    "Jeep": "https://www.jeep.com/incentives-offers.html",
    "Kia": "https://www.kia.com/us/en/special-offers",
    "Lexus": "https://www.lexus.com/offers",
    "Lincoln": "https://www.lincoln.com/shopping/offers-incentives/",
    "Mazda": "https://www.mazdausa.com/shopping-tools/offers-and-incentives",
    "Mercedes-Benz": "https://www.mbusa.com/en/special-offers",
    "Nissan": "https://www.nissanusa.com/shopping-tools/offers-incentives",
    "Subaru": "https://www.subaru.com/shopping-tools/current-offers",
    "Toyota": "https://www.toyota.com/deals",
    "Volkswagen": "https://www.vw.com/en/shopping-tools/special-offers",
    "Volvo": "https://www.volvocars.com/us/shopping/offers/",
}

# Model-specific pages where incentives appear (SPAs hide offers on landing pages).
# Focus on high-value EV/PHEV models and popular vehicles most likely to have big incentives.
OEM_MODEL_PAGES: dict[str, list[str]] = {
    "Hyundai": [
        "https://www.hyundaiusa.com/us/en/vehicles/ioniq-5",
        "https://www.hyundaiusa.com/us/en/vehicles/ioniq-6",
        "https://www.hyundaiusa.com/us/en/vehicles/ioniq-9",
        "https://www.hyundaiusa.com/us/en/vehicles/tucson",
        "https://www.hyundaiusa.com/us/en/vehicles/santa-fe",
        "https://www.hyundaiusa.com/us/en/vehicles/elantra",
        "https://www.hyundaiusa.com/us/en/vehicles/sonata",
    ],
    "Kia": [
        "https://www.kia.com/us/en/ev6",
        "https://www.kia.com/us/en/ev9",
        "https://www.kia.com/us/en/sportage",
        "https://www.kia.com/us/en/telluride",
    ],
    "Toyota": [
        "https://www.toyota.com/bz4x",
        "https://www.toyota.com/rav4prime",
        "https://www.toyota.com/camry",
        "https://www.toyota.com/tacoma",
        "https://www.toyota.com/highlander",
    ],
    "Chevrolet": [
        "https://www.chevrolet.com/us/en/electric/equinox-ev",
        "https://www.chevrolet.com/us/en/electric/blazer-ev",
        "https://www.chevrolet.com/us/en/electric/silverado-ev",
        "https://www.chevrolet.com/us/en/trucks/silverado",
    ],
    "Ford": [
        "https://www.ford.com/trucks/f150/f150-lightning/",
        "https://www.ford.com/suvs-crossovers/mustang-mach-e/",
        "https://www.ford.com/trucks/f150/",
        "https://www.ford.com/suvs/explorer/",
    ],
    "Honda": [
        "https://www.honda.com/prologue",
        "https://www.honda.com/cr-v",
        "https://www.honda.com/civic",
    ],
    "Nissan": [
        "https://www.nissanusa.com/vehicles/electric-cars/ariya",
        "https://www.nissanusa.com/vehicles/electric-cars/leaf",
        "https://www.nissanusa.com/vehicles/crossovers-suvs/rogue",
    ],
    "Volkswagen": [
        "https://www.vw.com/en/models/id-4",
        "https://www.vw.com/en/models/id-buzz",
        "https://www.vw.com/en/models/atlas",
    ],
}

# Claude prompt for extracting incentive data from rendered page text
EXTRACTION_PROMPT = """You are an automotive incentive data extractor. Given the rendered text content from a car manufacturer's website page, extract ALL current incentive programs.

For each incentive found, return a JSON object with these fields:
- name: descriptive name (e.g. "2026 IONIQ 5 Dealer Choice Bonus Cash")
- make: the manufacturer name (provided)
- model: specific model name, or null if applies to all models
- incentive_type: one of "cash", "lease", "apr"
- amount: dollar amount for cash incentives, or null
- percentage: APR rate for financing offers, or null
- monthly_payment: monthly payment for lease offers, or null
- lease_term: months for lease term, or null
- due_at_signing: amount due at lease signing, or null
- start_date: in YYYY-MM-DD format, or null
- end_date: in YYYY-MM-DD format, or null
- description: brief description of the offer
- disclaimer: key restrictions/fine print, or null

Rules:
- Extract EVERY incentive/offer you can find, including cash back, bonus cash, APR specials, lease deals
- Pay special attention to large cash incentives ($2,000+) as these are the most valuable
- If a single offer applies to multiple trims, list it ONCE with the model name (not per-trim)
- Convert dates to YYYY-MM-DD format
- If amount says "up to $X", use X as the amount
- Return ONLY a JSON array of objects. No other text.
- If no incentives are found, return an empty array: []

The manufacturer is: {make}
The page URL is: {url}

Page text content:
{text}"""


def _fetch_oem_page(url: str) -> str | None:
    """Fetch an OEM page using Playwright in a thread (to avoid async conflict)."""
    import concurrent.futures

    def _run_playwright(target_url: str) -> str | None:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            logger.error("Playwright not installed")
            return None

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(target_url, timeout=30000, wait_until="domcontentloaded")
                page.wait_for_timeout(5000)
                text = page.inner_text("body")
                browser.close()

                if len(text.strip()) < 100:
                    logger.warning("Page %s rendered with very little text (%d chars)", target_url, len(text))
                    return None

                return text
        except Exception as e:
            logger.error("Playwright failed for %s: %s", target_url, e)
            return None

    # Run Playwright in a separate thread to avoid asyncio loop conflict
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_run_playwright, url)
        try:
            return future.result(timeout=60)
        except concurrent.futures.TimeoutError:
            logger.error("Playwright timed out for %s", url)
            return None


def _extract_incentives_with_gemini(make: str, page_text: str, url: str = "") -> list[dict]:
    """Use Google Gemini (free tier) to extract structured incentive data from rendered page text."""
    api_key = settings.gemini_api_key
    if not api_key:
        logger.error("GEMINI_API_KEY not configured — cannot extract incentives")
        return []

    # Truncate text to fit context
    if len(page_text) > 50_000:
        page_text = page_text[:50_000]

    prompt = EXTRACTION_PROMPT.format(make=make, text=page_text, url=url)

    try:
        with httpx.Client(timeout=120) as client:
            resp = client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}",
                headers={"content-type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.1,
                        "maxOutputTokens": 4096,
                    },
                },
            )
            resp.raise_for_status()
            data = resp.json()

        content = data["candidates"][0]["content"]["parts"][0]["text"]

        # Parse JSON from response — handle markdown code blocks
        content = content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1]  # remove ```json
            content = content.rsplit("```", 1)[0]  # remove trailing ```

        incentives = json.loads(content)
        if not isinstance(incentives, list):
            logger.warning("Gemini returned non-list for %s", make)
            return []

        return incentives

    except json.JSONDecodeError as e:
        logger.error("Failed to parse Gemini response for %s: %s", make, e)
        return []
    except Exception as e:
        logger.error("Gemini API error for %s: %s", make, e)
        return []


def _incentive_to_db_dict(make: str, inc: dict) -> dict:
    """Convert an extracted incentive dict to match the incentive_programs schema."""
    inc_type = inc.get("incentive_type", "cash")

    if inc_type == "apr":
        value_type = "rate_reduction"
    else:
        value_type = "fixed"

    purchase_types = {
        "cash": ["cash"],
        "lease": ["lease"],
        "apr": ["finance"],
    }

    claim_mechanism = "lease_reduction" if inc_type == "lease" else "point_of_sale"

    vehicle_criteria: dict = {"make": make}
    if inc.get("model"):
        vehicle_criteria["model"] = inc["model"]

    return {
        "name": inc.get("name", f"{make} Offer"),
        "type": "manufacturer",
        "source_authority": f"{make} (via OEM Monitor)",
        "geographic_scope": "national",
        "eligible_states": [],
        "eligible_zips": [],
        "eligible_purchase_types": purchase_types.get(inc_type, ["cash", "finance", "lease"]),
        "vehicle_criteria": vehicle_criteria,
        "buyer_criteria": {},
        "incentive_value_type": value_type,
        "incentive_amount": inc.get("amount"),
        "incentive_max_amount": inc.get("amount"),
        "incentive_percentage": inc.get("percentage"),
        "start_date": inc.get("start_date"),
        "end_date": inc.get("end_date"),
        "application_deadline": None,
        "funding_status": "open",
        "claim_mechanism": claim_mechanism,
        "last_verified": datetime.now(timezone.utc).isoformat(),
        "source_url": OEM_OFFERS_PAGES.get(make, ""),
        "confidence_score": 0.90,
        "is_active": True,
        "description": inc.get("description", ""),
        "disclaimer": inc.get("disclaimer"),
    }


def _parse_date(val: str | None) -> datetime | None:
    """Parse a date string to datetime."""
    if not val:
        return None
    try:
        return datetime.fromisoformat(val).replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        pass
    try:
        return datetime.strptime(val, "%m/%d/%Y").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def monitor_oem_incentives() -> dict:
    """Fetch OEM offers pages, extract incentives via Claude, and upsert to DB."""
    import asyncio
    return asyncio.run(_monitor_async())


async def _monitor_async() -> dict:
    """Core async monitor logic."""
    engine = create_async_engine(DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    all_items: list[dict] = []
    makes_processed = 0
    makes_failed = 0

    seen_names: set[str] = set()

    for make, url in OEM_OFFERS_PAGES.items():
        # Collect all pages to check for this make
        pages_to_check = [(url, "offers")]
        for model_url in OEM_MODEL_PAGES.get(make, []):
            pages_to_check.append((model_url, "model"))

        make_count = 0
        make_ok = False

        for page_url, page_type in pages_to_check:
            logger.info("Fetching %s %s page: %s", make, page_type, page_url)

            page_text = _fetch_oem_page(page_url)
            if not page_text:
                continue

            make_ok = True

            # Skip pages with too little rendered content (SPA shells with no data)
            if len(page_text.strip()) < 500:
                logger.info("Skipping %s %s page — too little content (%d chars)", make, page_type, len(page_text))
                continue

            logger.info("Extracting incentives for %s from %s (%d chars)", make, page_type, len(page_text))

            # Rate limit: Gemini free tier is 10 RPM — space calls 8s apart
            time.sleep(8)

            raw_incentives = _extract_incentives_with_gemini(make, page_text, url=page_url)

            for raw in raw_incentives:
                item = _incentive_to_db_dict(make, raw)
                # Dedupe across pages
                if item["name"] not in seen_names:
                    seen_names.add(item["name"])
                    all_items.append(item)
                    make_count += 1

        if make_ok:
            makes_processed += 1
        else:
            makes_failed += 1

        logger.info("Extracted %d unique incentives for %s", make_count, make)

    logger.info("OEM Monitor: %d incentives from %d makes (%d failed)",
                len(all_items), makes_processed, makes_failed)

    # Upsert to database
    alerts: list[str] = []
    inserted = 0
    updated = 0

    async with session_factory() as session:
        # Load existing programs for diff detection
        rows = (await session.execute(text("SELECT * FROM incentive_programs"))).mappings().all()
        existing_by_name = {r["name"]: dict(r) for r in rows}

        for item in all_items:
            name = item.get("name", "")
            if not name:
                continue

            if name in existing_by_name:
                existing = existing_by_name[name]
                # Check if amount changed significantly
                old_amount = existing.get("incentive_amount")
                new_amount = item.get("incentive_amount")

                if (
                    old_amount is not None
                    and new_amount is not None
                    and abs(float(new_amount) - float(old_amount)) > 100
                ):
                    alert = f"[OEM CHANGE] {name}: ${old_amount} -> ${new_amount}"
                    alerts.append(alert)
                    logger.warning(alert)

                # Update existing record
                now = datetime.now(timezone.utc)
                await session.execute(
                    text("""
                        UPDATE incentive_programs
                        SET incentive_amount = COALESCE(:amount, incentive_amount),
                            incentive_max_amount = COALESCE(:max_amount, incentive_max_amount),
                            incentive_percentage = COALESCE(:percentage, incentive_percentage),
                            is_active = true,
                            last_verified = :now,
                            start_date = COALESCE(:start_date, start_date),
                            end_date = COALESCE(:end_date, end_date),
                            updated_at = :now
                        WHERE name = :name
                    """),
                    {
                        "name": name,
                        "amount": item.get("incentive_amount"),
                        "max_amount": item.get("incentive_max_amount"),
                        "percentage": item.get("incentive_percentage"),
                        "start_date": _parse_date(item.get("start_date")),
                        "end_date": _parse_date(item.get("end_date")),
                        "now": now,
                    },
                )
                updated += 1
            else:
                # New incentive — insert
                alert = f"[OEM NEW] {name}: ${item.get('incentive_amount') or 'N/A'}"
                alerts.append(alert)
                logger.info(alert)

                now = datetime.now(timezone.utc)
                start_date = _parse_date(item.get("start_date"))
                end_date = _parse_date(item.get("end_date"))

                await session.execute(
                    text("""
                        INSERT INTO incentive_programs (
                            id, name, type, source_authority, geographic_scope,
                            eligible_states, eligible_zips, eligible_purchase_types,
                            vehicle_criteria, buyer_criteria,
                            incentive_value_type, incentive_amount,
                            incentive_max_amount, incentive_percentage,
                            stackable_with, mutually_exclusive_with,
                            start_date, end_date, application_deadline,
                            funding_status, claim_mechanism,
                            last_verified, source_url, confidence_score,
                            is_active, created_at, updated_at
                        ) VALUES (
                            :id, :name, :type, :source_authority, :geographic_scope,
                            :eligible_states, :eligible_zips, :eligible_purchase_types,
                            :vehicle_criteria, :buyer_criteria,
                            :incentive_value_type, :incentive_amount,
                            :incentive_max_amount, :incentive_percentage,
                            :stackable_with, :mutually_exclusive_with,
                            :start_date, :end_date, :application_deadline,
                            :funding_status, :claim_mechanism,
                            :last_verified, :source_url, :confidence_score,
                            :is_active, :created_at, :updated_at
                        )
                        ON CONFLICT (name) DO UPDATE SET
                            incentive_amount = EXCLUDED.incentive_amount,
                            incentive_max_amount = EXCLUDED.incentive_max_amount,
                            incentive_percentage = EXCLUDED.incentive_percentage,
                            eligible_purchase_types = EXCLUDED.eligible_purchase_types,
                            is_active = EXCLUDED.is_active,
                            last_verified = EXCLUDED.last_verified,
                            confidence_score = EXCLUDED.confidence_score,
                            updated_at = EXCLUDED.updated_at
                    """),
                    {
                        "id": str(uuid.uuid4()),
                        "name": name,
                        "type": item.get("type", "manufacturer"),
                        "source_authority": item.get("source_authority", ""),
                        "geographic_scope": item.get("geographic_scope", "national"),
                        "eligible_states": item.get("eligible_states", []),
                        "eligible_zips": item.get("eligible_zips", []),
                        "eligible_purchase_types": item.get("eligible_purchase_types", ["cash", "finance", "lease"]),
                        "vehicle_criteria": json.dumps(item.get("vehicle_criteria", {})),
                        "buyer_criteria": json.dumps(item.get("buyer_criteria", {})),
                        "incentive_value_type": item.get("incentive_value_type", "fixed"),
                        "incentive_amount": item.get("incentive_amount"),
                        "incentive_max_amount": item.get("incentive_max_amount"),
                        "incentive_percentage": item.get("incentive_percentage"),
                        "stackable_with": [],
                        "mutually_exclusive_with": [],
                        "start_date": start_date or now,
                        "end_date": end_date,
                        "application_deadline": None,
                        "funding_status": item.get("funding_status", "open"),
                        "claim_mechanism": item.get("claim_mechanism", "point_of_sale"),
                        "last_verified": now,
                        "source_url": item.get("source_url", ""),
                        "confidence_score": item.get("confidence_score", 0.90),
                        "is_active": True,
                        "created_at": now,
                        "updated_at": now,
                    },
                )
                inserted += 1

        # Mark OEM Monitor-sourced programs not seen in this run as stale
        all_names = {item.get("name") for item in all_items if item.get("name")}
        stale_count = 0
        for name, existing in existing_by_name.items():
            source = existing.get("source_authority", "")
            if (
                name not in all_names
                and existing.get("is_active")
                and "OEM Monitor" in source
            ):
                await session.execute(
                    text("""
                        UPDATE incentive_programs
                        SET is_active = false, updated_at = :now
                        WHERE name = :name
                    """),
                    {"name": name, "now": datetime.now(timezone.utc)},
                )
                stale_count += 1
                alerts.append(f"[OEM STALE] Deactivated: {name}")

        if stale_count:
            logger.info("Deactivated %d stale OEM Monitor programs", stale_count)

        await session.commit()

    await engine.dispose()

    result = {
        "makes_processed": makes_processed,
        "makes_failed": makes_failed,
        "total_incentives": len(all_items),
        "inserted": inserted,
        "updated": updated,
        "stale_deactivated": stale_count if 'stale_count' in dir() else 0,
        "alerts": alerts,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    logger.info(
        "OEM Monitor complete: %d incentives, %d new, %d updated, %d alerts",
        len(all_items), inserted, updated, len(alerts),
    )

    return result


# Celery task wrapper
try:
    from celery import shared_task

    @shared_task(name="monitor_oem_incentives", bind=True, max_retries=1, default_retry_delay=600)
    def monitor_oem_incentives_task(self):
        try:
            return monitor_oem_incentives()
        except Exception as exc:
            logger.error("OEM Monitor task failed: %s", exc)
            raise self.retry(exc=exc)

except ImportError:
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = monitor_oem_incentives()
    print(json.dumps(result, indent=2))
