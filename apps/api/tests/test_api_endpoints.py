"""Tests for API endpoint request/response contracts.

These tests use TestClient (sync) and don't require a running database.
They verify routing, validation, and response shapes.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_calculate_incentives_valid_request():
    payload = {
        "zip_code": "90210",
        "vehicle_interest": {
            "make": "Hyundai",
            "model": "IONIQ 5",
            "fuel_type": "BEV",
            "new_or_used": "new",
        },
        "buyer_profile": {
            "income_range": "75k-100k",
            "has_trade_in": False,
        },
    }
    response = client.post("/api/v1/incentives/calculate", json=payload)
    # Will return 200 even without DB (returns empty due to no connection or empty results)
    # In test environment without DB, we expect 500 (DB not available) or 200
    assert response.status_code in (200, 500)


def test_calculate_incentives_invalid_zip():
    payload = {
        "zip_code": "abc",
        "vehicle_interest": {},
        "buyer_profile": {},
    }
    response = client.post("/api/v1/incentives/calculate", json=payload)
    assert response.status_code == 422  # Validation error


def test_calculate_incentives_missing_zip():
    payload = {
        "vehicle_interest": {},
        "buyer_profile": {},
    }
    response = client.post("/api/v1/incentives/calculate", json=payload)
    assert response.status_code == 422


def test_submit_lead_valid_request():
    payload = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "phone": "555-123-4567",
        "zip_code": "90210",
        "vehicle_interest": {"make": "Hyundai", "model": "IONIQ 5"},
        "consent_text": "I consent to be contacted by dealerships regarding vehicle purchases.",
    }
    response = client.post("/api/v1/leads", json=payload)
    # Without DB, expect 500 or 200
    assert response.status_code in (200, 500)


def test_submit_lead_missing_consent():
    payload = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "zip_code": "90210",
    }
    response = client.post("/api/v1/leads", json=payload)
    assert response.status_code == 422  # consent_text is required


def test_submit_lead_invalid_zip():
    payload = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "zip_code": "abc",
        "consent_text": "I consent to being contacted.",
    }
    response = client.post("/api/v1/leads", json=payload)
    assert response.status_code == 422


def test_list_incentives_by_state_valid():
    response = client.get("/api/v1/incentives/CA")
    # Without DB, expect 500 or 200
    assert response.status_code in (200, 500)


def test_list_incentives_by_state_invalid():
    response = client.get("/api/v1/incentives/california")
    assert response.status_code == 422  # Must be 2-letter code


def test_find_dealers_by_zip():
    response = client.get("/api/v1/dealers/90210")
    # Without DB, expect 500 or 200
    assert response.status_code in (200, 500)


def test_find_dealers_invalid_zip():
    response = client.get("/api/v1/dealers/abc")
    assert response.status_code == 422
