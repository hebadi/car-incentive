"""Tests for the lead scoring pipeline."""

from datetime import datetime, timedelta, timezone

from app.services.lead_scorer import score_lead, classify_tier, _score_intent, _score_incentive_match, _score_buyer_readiness, _score_data_completeness


# --- Tier classification ---

def test_classify_tier_hot():
    assert classify_tier(80) == "hot"
    assert classify_tier(100) == "hot"


def test_classify_tier_warm():
    assert classify_tier(50) == "warm"
    assert classify_tier(79) == "warm"


def test_classify_tier_nurture():
    assert classify_tier(20) == "nurture"
    assert classify_tier(49) == "nurture"


def test_classify_tier_unqualified():
    assert classify_tier(0) == "unqualified"
    assert classify_tier(19) == "unqualified"


# --- Intent scoring ---

def test_intent_calculator_only():
    assert _score_intent({}) == 15  # calculator_completed defaults to True


def test_intent_with_vehicle_model():
    assert _score_intent({"vehicle_interest": {"model": "IONIQ 5"}}) == 25


def test_intent_with_return_visit():
    assert _score_intent({"return_visit": True}) == 25


def test_intent_capped_at_40():
    lead = {
        "vehicle_interest": {"model": "IONIQ 5"},
        "trade_in_estimated": True,
        "return_visit": True,
    }
    assert _score_intent(lead) == 40  # 15 + 10 + 10 + 10 = 45, capped at 40


# --- Incentive match scoring ---

def test_match_no_incentives():
    assert _score_incentive_match({"total_savings": 0, "incentives": []}) == 0


def test_match_high_savings():
    result = {"total_savings": 6000, "incentives": [{"id": "1"}]}
    assert _score_incentive_match(result) == 20  # 15 (savings) + 5 (1 incentive)


def test_match_three_plus_incentives():
    result = {
        "total_savings": 8000,
        "incentives": [{"id": "1"}, {"id": "2"}, {"id": "3"}],
    }
    assert _score_incentive_match(result) == 25  # 15 + 10


def test_match_expiring_incentive():
    soon = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    result = {
        "total_savings": 1000,
        "incentives": [{"id": "1", "end_date": soon}],
    }
    score = _score_incentive_match(result)
    assert score >= 15  # 5 (1 incentive) + 10 (expiring)


def test_match_depleting_funding():
    result = {
        "total_savings": 1000,
        "incentives": [{"id": "1", "funding_status": "waitlisted"}],
    }
    score = _score_incentive_match(result)
    assert score >= 15  # 5 (1 incentive) + 10 (depleting)


# --- Buyer readiness ---

def test_readiness_minimal():
    assert _score_buyer_readiness({}) == 0


def test_readiness_phone():
    assert _score_buyer_readiness({"phone": "555-1234"}) == 10


def test_readiness_full():
    lead = {
        "phone": "555-1234",
        "full_address": "123 Main St",
        "purchase_timeline": "within_30_days",
        "has_trade_in": True,
    }
    assert _score_buyer_readiness(lead) == 20  # Capped


# --- Data completeness ---

def test_completeness_minimal():
    assert _score_data_completeness({}) == 0


def test_completeness_required_fields():
    lead = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "zip_code": "90210",
    }
    assert _score_data_completeness(lead) == 5


def test_completeness_full():
    lead = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "zip_code": "90210",
        "income_range": "75k-100k",
        "vehicle_interest": {"make": "Hyundai"},
    }
    assert _score_data_completeness(lead) == 10  # Capped


# --- End-to-end scoring ---

def test_score_lead_minimal():
    score, tier = score_lead({}, {"total_savings": 0, "incentives": []})
    assert score == 15  # calculator use only
    assert tier == "unqualified"


def test_score_lead_hot():
    lead = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "zip_code": "90210",
        "phone": "555-1234",
        "full_address": "123 Main St",
        "has_trade_in": True,
        "income_range": "50k-75k",
        "vehicle_interest": {"make": "Hyundai", "model": "IONIQ 5"},
        "purchase_timeline": "within_30_days",
    }
    incentive_result = {
        "total_savings": 8000,
        "incentives": [{"id": "1"}, {"id": "2"}, {"id": "3"}],
    }
    score, tier = score_lead(lead, incentive_result)
    assert score >= 80
    assert tier == "hot"


def test_score_lead_warm():
    lead = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "zip_code": "10001",
        "phone": "555-5678",
        "full_address": "456 Oak Ave, New York, NY",
        "income_range": "50k-75k",
        "vehicle_interest": {"make": "Toyota"},
    }
    incentive_result = {
        "total_savings": 3000,
        "incentives": [{"id": "1"}],
    }
    score, tier = score_lead(lead, incentive_result)
    assert 50 <= score < 80
    assert tier == "warm"
