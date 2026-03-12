"""Lead scoring service - rule-based scoring for MVP.

Weighted 0-100 model:
- Intent signals: 40%
- Incentive match quality: 30%
- Buyer readiness: 20%
- Data completeness: 10%
"""

from __future__ import annotations

from datetime import datetime, timezone


def score_lead(lead_data: dict, incentive_result: dict) -> tuple[int, str]:
    """Score a lead (0-100) and assign a tier.

    Returns (score, tier) tuple.
    """
    intent = _score_intent(lead_data)
    match_quality = _score_incentive_match(incentive_result)
    readiness = _score_buyer_readiness(lead_data)
    completeness = _score_data_completeness(lead_data)

    raw = intent + match_quality + readiness + completeness
    score = min(100, max(0, raw))

    tier = classify_tier(score)
    return score, tier


def classify_tier(score: int) -> str:
    """Return tier classification based on score."""
    if score >= 80:
        return "hot"
    elif score >= 50:
        return "warm"
    elif score >= 20:
        return "nurture"
    return "unqualified"


def _score_intent(lead_data: dict) -> int:
    """Intent signals (up to 40 points)."""
    points = 0

    # Used incentive calculator (always true if submitting via the calculator flow)
    if lead_data.get("calculator_completed", True):
        points += 15

    # Viewed/specified a specific vehicle
    vi = lead_data.get("vehicle_interest", {})
    if vi.get("model"):
        points += 10

    # Used trade-in estimator
    if lead_data.get("trade_in_estimated"):
        points += 10

    # Return visit within 7 days
    if lead_data.get("return_visit"):
        points += 10

    return min(40, points)


def _score_incentive_match(incentive_result: dict) -> int:
    """Incentive match quality (up to 30 points)."""
    points = 0

    total_savings = incentive_result.get("total_savings", 0)
    if total_savings >= 5000:
        points += 15
    elif total_savings >= 2000:
        points += 8

    num_incentives = len(incentive_result.get("incentives", []))
    if num_incentives >= 3:
        points += 10
    elif num_incentives >= 1:
        points += 5

    # Time-sensitive incentive (expiring within 60 days)
    for inc in incentive_result.get("incentives", []):
        end_date = inc.get("end_date")
        if end_date:
            try:
                if isinstance(end_date, str):
                    ed = datetime.fromisoformat(end_date)
                else:
                    ed = end_date
                if ed.tzinfo is None:
                    ed = ed.replace(tzinfo=timezone.utc)
                days_left = (ed - datetime.now(timezone.utc)).days
                if 0 < days_left <= 60:
                    points += 10
                    break
            except (ValueError, TypeError):
                pass

    # Depleting funding
    for inc in incentive_result.get("incentives", []):
        if inc.get("funding_status") in ("waitlisted", "depleted"):
            points += 10
            break

    return min(30, points)


def _score_buyer_readiness(lead_data: dict) -> int:
    """Buyer readiness (up to 20 points)."""
    points = 0

    if lead_data.get("phone"):
        points += 10

    if lead_data.get("full_address"):
        points += 5

    timeline = lead_data.get("purchase_timeline", "")
    if timeline and timeline in ("immediate", "within_30_days", "0-30"):
        points += 10

    if lead_data.get("has_trade_in"):
        points += 5

    return min(20, points)


def _score_data_completeness(lead_data: dict) -> int:
    """Data completeness (up to 10 points)."""
    points = 0

    required_fields = ["first_name", "last_name", "email", "zip_code"]
    if all(lead_data.get(f) for f in required_fields):
        points += 5

    if lead_data.get("income_range"):
        points += 3

    vi = lead_data.get("vehicle_interest", {})
    if vi.get("make") or vi.get("model"):
        points += 5

    return min(10, points)
