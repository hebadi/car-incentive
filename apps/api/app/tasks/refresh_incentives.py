"""
Celery task for refreshing incentive data from scrapers and APIs.

Features:
  - Runs all configured scrapers and the MarketCheck API client
  - Diff detection (flags changes from previous run)
  - Alert generation for significant changes
  - Idempotent upsert into the incentive_programs table

Usage (standalone):
    python -m app.tasks.refresh_incentives

Usage (Celery):
    from app.tasks.refresh_incentives import refresh_incentives
    refresh_incentives.delay()
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
import tempfile
from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.services.marketcheck_client import MarketCheckClient

logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    settings.database_url,
)

# Spider modules to run (add new spiders here)
SPIDER_MODULES = [
    "scrapers.nyserda_spider",
]

# OEM makes to query via MarketCheck (matches calculator VEHICLE_MODELS)
MARKETCHECK_MAKES = [
    "Acura", "Audi", "BMW", "Buick", "Cadillac", "Chevrolet", "Chrysler",
    "Dodge", "Fiat", "Ford", "Genesis", "GMC", "Honda", "Hyundai",
    "Infiniti", "Jaguar", "Jeep", "Kia", "Land Rover", "Lexus",
    "Lincoln", "Lucid", "Mazda", "Mercedes-Benz", "Mini", "Mitsubishi",
    "Nissan", "Polestar", "Porsche", "Ram", "Rivian", "Subaru",
    "Tesla", "Toyota", "Volkswagen", "Volvo",
]


def _parse_date(val: str | None) -> datetime | None:
    """Parse a date string (ISO or MM/DD/YYYY) to a datetime, or return None."""
    if val is None:
        return None
    if isinstance(val, datetime):
        return val
    try:
        return datetime.fromisoformat(val).replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        pass
    try:
        return datetime.strptime(val, "%m/%d/%Y").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def _run_spiders() -> list[dict]:
    """Run all Scrapy spiders and collect their output."""
    all_items: list[dict] = []

    for module in SPIDER_MODULES:
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            output_path = f.name

        try:
            result = subprocess.run(
                ["scrapy", "runspider", module.replace(".", "/") + ".py", "-o", output_path, "-t", "json"],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=os.path.join(os.path.dirname(__file__), "..", ".."),
            )

            if result.returncode != 0:
                logger.error("Spider %s failed: %s", module, result.stderr[:500])
                continue

            with open(output_path) as f:
                items = json.load(f)
            all_items.extend(items)
            logger.info("Spider %s yielded %d items", module, len(items))

        except subprocess.TimeoutExpired:
            logger.error("Spider %s timed out", module)
        except Exception as e:
            logger.error("Spider %s error: %s", module, e)
        finally:
            try:
                os.unlink(output_path)
            except OSError:
                pass

    return all_items


def _fetch_marketcheck_incentives() -> list[dict]:
    """Fetch OEM incentives from MarketCheck API for all makes and offer types."""
    client = MarketCheckClient()
    all_items: list[dict] = []
    seen_names: set[str] = set()

    for make in MARKETCHECK_MAKES:
        make_count = 0
        # Query each offer type separately for full coverage
        for offer_type in ("cash", "lease", "apr"):
            try:
                incentives = client.get_oem_incentives(make, offer_type=offer_type)
                for inc in incentives:
                    program = client.incentive_to_program_dict(inc)
                    # Dedupe across offer types (same name = same program)
                    if program["name"] not in seen_names:
                        seen_names.add(program["name"])
                        all_items.append(program)
                        make_count += 1
            except Exception as e:
                logger.error("MarketCheck error for %s/%s: %s", make, offer_type, e)

        logger.info("MarketCheck: %d incentives for %s", make_count, make)

    return all_items


def _detect_diffs(existing: dict, new_item: dict) -> list[str]:
    """Compare an existing DB record against a scraped item and return change descriptions."""
    changes = []

    if (
        new_item.get("incentive_amount") is not None
        and existing.get("incentive_amount") is not None
        and float(new_item["incentive_amount"]) != float(existing["incentive_amount"])
    ):
        changes.append(
            f"Amount changed: ${existing['incentive_amount']} -> ${new_item['incentive_amount']}"
        )

    new_status = new_item.get("funding_status", "open")
    old_status = existing.get("funding_status", "open")
    if new_status != old_status:
        changes.append(f"Funding status changed: {old_status} -> {new_status}")

    new_active = new_item.get("is_active", True)
    old_active = existing.get("is_active", True)
    if new_active != old_active:
        changes.append(f"Active status changed: {old_active} -> {new_active}")

    return changes


async def _refresh_async() -> dict:
    """Core async refresh logic."""
    engine = create_async_engine(DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # 1. Collect data from all sources
    spider_items = _run_spiders()
    marketcheck_items = _fetch_marketcheck_incentives()
    all_items = spider_items + marketcheck_items

    logger.info("Collected %d items total (%d spider, %d MarketCheck)",
                len(all_items), len(spider_items), len(marketcheck_items))

    alerts: list[str] = []
    updated = 0
    inserted = 0

    async with session_factory() as session:
        # Load existing programs keyed by name for diff detection
        rows = (await session.execute(text("SELECT * FROM incentive_programs"))).mappings().all()
        existing_by_name = {r["name"]: dict(r) for r in rows}

        for item in all_items:
            name = item.get("name", "")
            if not name:
                continue

            if name in existing_by_name:
                # Diff detection
                diffs = _detect_diffs(existing_by_name[name], item)
                if diffs:
                    for d in diffs:
                        alert_msg = f"[CHANGE] {name}: {d}"
                        alerts.append(alert_msg)
                        logger.warning(alert_msg)

                    # Update existing record
                    await session.execute(
                        text("""
                            UPDATE incentive_programs
                            SET incentive_amount = :amount,
                                incentive_max_amount = :max_amount,
                                incentive_percentage = :percentage,
                                funding_status = :funding_status,
                                is_active = :is_active,
                                last_verified = :last_verified,
                                confidence_score = :confidence_score,
                                start_date = COALESCE(:start_date, start_date),
                                end_date = COALESCE(:end_date, end_date),
                                updated_at = :updated_at
                            WHERE name = :name
                        """),
                        {
                            "name": name,
                            "amount": item.get("incentive_amount"),
                            "max_amount": item.get("incentive_max_amount"),
                            "percentage": item.get("incentive_percentage"),
                            "funding_status": item.get("funding_status", "open"),
                            "is_active": item.get("is_active", True),
                            "last_verified": datetime.now(timezone.utc),
                            "confidence_score": item.get("confidence_score", 0.7),
                            "start_date": _parse_date(item.get("start_date")),
                            "end_date": _parse_date(item.get("end_date")),
                            "updated_at": datetime.now(timezone.utc),
                        },
                    )
                    updated += 1
                else:
                    # Just bump last_verified
                    await session.execute(
                        text("""
                            UPDATE incentive_programs
                            SET last_verified = :now, updated_at = :now
                            WHERE name = :name
                        """),
                        {"name": name, "now": datetime.now(timezone.utc)},
                    )
            else:
                # New program -- insert it
                alert_msg = f"[NEW] Discovered new incentive: {name}"
                alerts.append(alert_msg)
                logger.info(alert_msg)

                import uuid
                now = datetime.now(timezone.utc)
                start_date = _parse_date(item.get("start_date"))
                end_date = _parse_date(item.get("end_date"))
                app_deadline = _parse_date(item.get("application_deadline"))

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
                            funding_status = EXCLUDED.funding_status,
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
                        "stackable_with": item.get("stackable_with", []),
                        "mutually_exclusive_with": item.get("mutually_exclusive_with", []),
                        "start_date": start_date or now,
                        "end_date": end_date,
                        "application_deadline": app_deadline,
                        "funding_status": item.get("funding_status", "open"),
                        "claim_mechanism": item.get("claim_mechanism", "point_of_sale"),
                        "last_verified": now,
                        "source_url": item.get("source_url", ""),
                        "confidence_score": item.get("confidence_score", 0.7),
                        "is_active": item.get("is_active", True),
                        "created_at": now,
                        "updated_at": now,
                    },
                )
                inserted += 1

        # Mark MarketCheck-sourced programs not seen in this refresh as inactive.
        # Only deactivate programs originally from MarketCheck — never touch
        # manually curated seed data or programs from other sources.
        all_names = {item.get("name") for item in all_items if item.get("name")}
        stale_count = 0
        for name, existing in existing_by_name.items():
            source = existing.get("source_authority", "")
            if (
                name not in all_names
                and existing.get("is_active")
                and "MarketCheck" in source
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
                alerts.append(f"[STALE] Deactivated: {name}")

        if stale_count:
            logger.info("Deactivated %d stale manufacturer programs", stale_count)

        await session.commit()

    await engine.dispose()

    result = {
        "total_items": len(all_items),
        "updated": updated,
        "inserted": inserted,
        "alerts": alerts,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    logger.info("Refresh complete: %d items, %d updated, %d new, %d alerts",
                len(all_items), updated, inserted, len(alerts))

    return result


def refresh_incentives() -> dict:
    """Synchronous entry point (for Celery or standalone use)."""
    import asyncio
    return asyncio.run(_refresh_async())


# Celery task wrapper (when Celery is configured)
try:
    from celery import shared_task

    @shared_task(name="refresh_incentives", bind=True, max_retries=2, default_retry_delay=300)
    def refresh_incentives_task(self):
        try:
            return refresh_incentives()
        except Exception as exc:
            logger.error("Refresh task failed: %s", exc)
            raise self.retry(exc=exc)

except ImportError:
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = refresh_incentives()
    print(json.dumps(result, indent=2))
