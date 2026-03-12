"""Tests for the incentive matching engine."""

import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from app.services.incentive_matcher import (
    filter_by_geography,
    filter_by_vehicle,
    filter_by_buyer,
    resolve_stacking,
    compute_value,
    generate_disclaimers,
    zip_to_state,
)


def _make_incentive(**overrides) -> MagicMock:
    """Create a mock IncentiveProgram with sensible defaults."""
    defaults = {
        "id": uuid.uuid4(),
        "name": "Test Incentive",
        "type": "state",
        "source_authority": "Test Authority",
        "geographic_scope": "state",
        "eligible_states": ["CA"],
        "eligible_zips": [],
        "vehicle_criteria": {},
        "buyer_criteria": {},
        "incentive_value_type": "fixed",
        "incentive_amount": 2000,
        "incentive_max_amount": None,
        "incentive_percentage": None,
        "stackable_with": [],
        "mutually_exclusive_with": [],
        "start_date": datetime(2025, 1, 1, tzinfo=timezone.utc),
        "end_date": datetime(2027, 12, 31, tzinfo=timezone.utc),
        "application_deadline": None,
        "funding_status": "open",
        "claim_mechanism": "point_of_sale",
        "last_verified": datetime.now(timezone.utc),
        "source_url": "https://example.com",
        "confidence_score": 0.9,
        "is_active": True,
    }
    defaults.update(overrides)
    mock = MagicMock()
    for k, v in defaults.items():
        setattr(mock, k, v)
    return mock


# --- zip_to_state ---

def test_zip_to_state_california():
    assert zip_to_state("90210") == "CA"


def test_zip_to_state_new_york():
    assert zip_to_state("10001") == "NY"


def test_zip_to_state_unknown():
    assert zip_to_state("00000") is None


# --- filter_by_geography ---

def test_geo_filter_state_match():
    inc = _make_incentive(geographic_scope="state", eligible_states=["CA"])
    result = filter_by_geography([inc], "90210")
    assert len(result) == 1


def test_geo_filter_state_no_match():
    inc = _make_incentive(geographic_scope="state", eligible_states=["NY"])
    result = filter_by_geography([inc], "90210")
    assert len(result) == 0


def test_geo_filter_national():
    inc = _make_incentive(geographic_scope="national", eligible_states=[])
    result = filter_by_geography([inc], "90210")
    assert len(result) == 1


def test_geo_filter_zip_match():
    inc = _make_incentive(geographic_scope="zip", eligible_zips=["90210"])
    result = filter_by_geography([inc], "90210")
    assert len(result) == 1


def test_geo_filter_zip_no_match():
    inc = _make_incentive(geographic_scope="zip", eligible_zips=["10001"])
    result = filter_by_geography([inc], "90210")
    assert len(result) == 0


# --- filter_by_vehicle ---

def test_vehicle_filter_fuel_type_match():
    inc = _make_incentive(vehicle_criteria={"fuel_types": ["BEV", "PHEV"]})
    result = filter_by_vehicle([inc], {"fuel_type": "BEV"})
    assert len(result) == 1


def test_vehicle_filter_fuel_type_no_match():
    inc = _make_incentive(vehicle_criteria={"fuel_types": ["BEV"]})
    result = filter_by_vehicle([inc], {"fuel_type": "ICE"})
    assert len(result) == 0


def test_vehicle_filter_make_match():
    inc = _make_incentive(vehicle_criteria={"make": ["Hyundai", "Kia"]})
    result = filter_by_vehicle([inc], {"make": "Hyundai"})
    assert len(result) == 1


def test_vehicle_filter_msrp_cap():
    inc = _make_incentive(vehicle_criteria={"msrp_cap": 55000})
    assert len(filter_by_vehicle([inc], {"msrp": 50000})) == 1
    assert len(filter_by_vehicle([inc], {"msrp": 60000})) == 0


def test_vehicle_filter_new_used():
    inc = _make_incentive(vehicle_criteria={"new_or_used": "new"})
    assert len(filter_by_vehicle([inc], {"new_or_used": "new"})) == 1
    assert len(filter_by_vehicle([inc], {"new_or_used": "used"})) == 0


def test_vehicle_filter_no_criteria():
    inc = _make_incentive(vehicle_criteria={})
    result = filter_by_vehicle([inc], {"fuel_type": "BEV"})
    assert len(result) == 1


def test_vehicle_filter_empty_vehicle():
    inc = _make_incentive(vehicle_criteria={"fuel_types": ["BEV"]})
    result = filter_by_vehicle([inc], {})
    assert len(result) == 1  # No vehicle info provided means we can't exclude


# --- filter_by_buyer ---

def test_buyer_filter_income_under_limit():
    inc = _make_incentive(buyer_criteria={"income_max": 100000})
    result = filter_by_buyer([inc], {"income_range": "50k-75k"})
    assert len(result) == 1


def test_buyer_filter_income_over_limit():
    inc = _make_incentive(buyer_criteria={"income_max": 50000})
    result = filter_by_buyer([inc], {"income_range": "75k-100k"})
    assert len(result) == 0


def test_buyer_filter_filing_status_limits():
    inc = _make_incentive(buyer_criteria={
        "income_max": 150000,
        "filing_status_limits": {"married_filing_jointly": 300000, "single": 150000},
    })
    # Married filing jointly with income 200-300k should pass the MFJ limit
    result = filter_by_buyer([inc], {"income_range": "200k-300k", "filing_status": "married_filing_jointly"})
    assert len(result) == 1

    # Single with income 200-300k should fail the single limit
    result = filter_by_buyer([inc], {"income_range": "200k-300k", "filing_status": "single"})
    assert len(result) == 0


def test_buyer_filter_trade_in_required():
    inc = _make_incentive(buyer_criteria={"trade_in_required": True})
    assert len(filter_by_buyer([inc], {"has_trade_in": True})) == 1
    assert len(filter_by_buyer([inc], {"has_trade_in": False})) == 0


def test_buyer_filter_affinity():
    inc = _make_incentive(buyer_criteria={"affinity_group": "military"})
    assert len(filter_by_buyer([inc], {"affinity_groups": ["military"]})) == 1
    assert len(filter_by_buyer([inc], {"affinity_groups": ["educator"]})) == 0
    assert len(filter_by_buyer([inc], {"affinity_groups": []})) == 0


# --- resolve_stacking ---

def test_stacking_no_exclusions():
    a = _make_incentive(name="A", incentive_amount=1000)
    b = _make_incentive(name="B", incentive_amount=2000)
    result = resolve_stacking([a, b])
    assert len(result) == 2


def test_stacking_mutual_exclusion_picks_higher():
    id_a = uuid.uuid4()
    id_b = uuid.uuid4()
    a = _make_incentive(id=id_a, name="Cash Rebate", incentive_amount=3000, mutually_exclusive_with=[id_b])
    b = _make_incentive(id=id_b, name="0% APR", incentive_value_type="rate_reduction", incentive_amount=0, incentive_percentage=5.0, mutually_exclusive_with=[id_a])
    result = resolve_stacking([a, b])
    assert len(result) == 1
    # rate_reduction on $35k at 5% for 5y/2 = $4375, which is > $3000
    assert result[0].name == "0% APR"


def test_stacking_mixed():
    id_a = uuid.uuid4()
    id_b = uuid.uuid4()
    a = _make_incentive(id=id_a, name="Rebate A", incentive_amount=1000, mutually_exclusive_with=[id_b])
    b = _make_incentive(id=id_b, name="Rebate B", incentive_amount=2000, mutually_exclusive_with=[id_a])
    c = _make_incentive(name="State Rebate", incentive_amount=3000)
    result = resolve_stacking([a, b, c])
    assert len(result) == 2
    names = {r.name for r in result}
    assert "Rebate B" in names  # Higher value
    assert "State Rebate" in names


# --- compute_value ---

def test_compute_value_fixed():
    inc = _make_incentive(incentive_value_type="fixed", incentive_amount=2500)
    assert compute_value(inc, {}) == 2500


def test_compute_value_tax_credit():
    inc = _make_incentive(incentive_value_type="tax_credit", incentive_amount=7500)
    assert compute_value(inc, {}) == 7500


def test_compute_value_percentage():
    inc = _make_incentive(
        incentive_value_type="percentage",
        incentive_percentage=30,
        incentive_max_amount=4000,
    )
    # 30% of $20000 = $6000, capped at $4000
    assert compute_value(inc, {"msrp": 20000}) == 4000
    # 30% of $10000 = $3000, under cap
    assert compute_value(inc, {"msrp": 10000}) == 3000


def test_compute_value_rate_reduction():
    inc = _make_incentive(
        incentive_value_type="rate_reduction",
        incentive_percentage=5.0,
    )
    # 5% on $35000 over 5y/2 = $4375
    assert compute_value(inc, {}) == pytest.approx(4375.0)


# --- generate_disclaimers ---

def test_disclaimers_low_confidence():
    inc = _make_incentive(confidence_score=0.6, source_url="https://example.com")
    disclaimers = generate_disclaimers([inc])
    assert any("not been recently verified" in d for d in disclaimers)


def test_disclaimers_depleted_funding():
    inc = _make_incentive(funding_status="depleted")
    disclaimers = generate_disclaimers([inc])
    assert any("depleted" in d for d in disclaimers)


def test_disclaimers_expiring_soon():
    inc = _make_incentive(end_date=datetime.now(timezone.utc) + timedelta(days=30))
    disclaimers = generate_disclaimers([inc])
    assert any("expires" in d.lower() for d in disclaimers)


def test_disclaimers_no_incentives():
    disclaimers = generate_disclaimers([])
    assert any("No matching incentives" in d for d in disclaimers)
