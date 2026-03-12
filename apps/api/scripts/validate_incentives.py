"""
Data validation script for incentive programs.

Checks:
  1. Stale data (last_verified > 30 days)
  2. Funding status anomalies (active but depleted/suspended)
  3. Amount anomalies (> 50% deviation from historical median)
  4. Expired programs still marked active

Usage:
    python -m scripts.validate_incentives
"""

import asyncio
import os
from datetime import datetime, timedelta, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/incentive_drive",
)


async def validate(database_url: str | None = None) -> dict:
    url = database_url or DATABASE_URL
    engine = create_async_engine(url, echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    report: dict = {
        "stale": [],
        "funding_anomalies": [],
        "amount_anomalies": [],
        "expired_but_active": [],
        "summary": {},
    }

    now = datetime.now(timezone.utc)
    stale_threshold = now - timedelta(days=30)

    async with session_factory() as session:
        rows = (await session.execute(text("SELECT * FROM incentive_programs"))).mappings().all()

        # Compute median amounts by type for anomaly detection
        amounts_by_type: dict[str, list[float]] = {}
        for r in rows:
            if r["incentive_amount"] is not None:
                amounts_by_type.setdefault(r["type"], []).append(float(r["incentive_amount"]))

        medians: dict[str, float] = {}
        for t, vals in amounts_by_type.items():
            sorted_vals = sorted(vals)
            mid = len(sorted_vals) // 2
            medians[t] = sorted_vals[mid]

        for r in rows:
            name = r["name"]
            pid = str(r["id"])

            # 1. Stale data
            if r["last_verified"] < stale_threshold:
                days_stale = (now - r["last_verified"]).days
                report["stale"].append({
                    "id": pid,
                    "name": name,
                    "last_verified": r["last_verified"].isoformat(),
                    "days_stale": days_stale,
                })

            # 2. Funding status anomalies
            if r["is_active"] and r["funding_status"] in ("depleted", "suspended"):
                report["funding_anomalies"].append({
                    "id": pid,
                    "name": name,
                    "funding_status": r["funding_status"],
                    "is_active": r["is_active"],
                    "issue": f"Program is marked active but funding is {r['funding_status']}",
                })

            # 3. Amount anomalies (> 50% deviation from median of its type)
            if r["incentive_amount"] is not None and r["type"] in medians:
                median = medians[r["type"]]
                if median > 0:
                    deviation = abs(float(r["incentive_amount"]) - median) / median
                    if deviation > 0.5:
                        report["amount_anomalies"].append({
                            "id": pid,
                            "name": name,
                            "amount": float(r["incentive_amount"]),
                            "type_median": median,
                            "deviation_pct": round(deviation * 100, 1),
                        })

            # 4. Expired programs still marked active
            if r["is_active"] and r["end_date"] is not None and r["end_date"] < now:
                report["expired_but_active"].append({
                    "id": pid,
                    "name": name,
                    "end_date": r["end_date"].isoformat(),
                })

    await engine.dispose()

    report["summary"] = {
        "total_programs": len(rows),
        "stale_count": len(report["stale"]),
        "funding_anomaly_count": len(report["funding_anomalies"]),
        "amount_anomaly_count": len(report["amount_anomalies"]),
        "expired_but_active_count": len(report["expired_but_active"]),
    }

    # Print report
    print("=" * 60)
    print("INCENTIVE DATA VALIDATION REPORT")
    print("=" * 60)
    print(f"Total programs: {report['summary']['total_programs']}")
    print()

    if report["stale"]:
        print(f"STALE DATA ({len(report['stale'])} programs):")
        for item in report["stale"]:
            print(f"  - {item['name']} ({item['days_stale']} days stale)")
        print()

    if report["funding_anomalies"]:
        print(f"FUNDING ANOMALIES ({len(report['funding_anomalies'])} programs):")
        for item in report["funding_anomalies"]:
            print(f"  - {item['name']}: {item['issue']}")
        print()

    if report["amount_anomalies"]:
        print(f"AMOUNT ANOMALIES ({len(report['amount_anomalies'])} programs):")
        for item in report["amount_anomalies"]:
            print(f"  - {item['name']}: ${item['amount']} ({item['deviation_pct']}% from median ${item['type_median']})")
        print()

    if report["expired_but_active"]:
        print(f"EXPIRED BUT ACTIVE ({len(report['expired_but_active'])} programs):")
        for item in report["expired_but_active"]:
            print(f"  - {item['name']} (ended {item['end_date']})")
        print()

    if not any([report["stale"], report["funding_anomalies"], report["amount_anomalies"], report["expired_but_active"]]):
        print("All checks passed.")

    print("=" * 60)
    return report


if __name__ == "__main__":
    asyncio.run(validate())
