from __future__ import annotations

import re

from pydantic import Field, field_validator

from app.schemas.incentives import CamelModel


class VehicleInterest(CamelModel):
    make: str | None = None
    model: str | None = None
    year: int | None = Field(None, ge=1990, le=2030)
    fuel_type: str | None = None
    new_or_used: str | None = None


class LeadSubmissionRequest(CamelModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=5, max_length=255)
    phone: str | None = Field(None, max_length=20)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email address")
        return v.lower().strip()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        if v is None:
            return v
        digits = re.sub(r"\D", "", v)
        if len(digits) not in (10, 11):
            raise ValueError("Phone must be 10 or 11 digits")
        return digits
    zip_code: str = Field(..., min_length=5, max_length=10, pattern=r"^\d{5}(-\d{4})?$")
    full_address: str | None = Field(None, max_length=500)
    income_range: str | None = None
    vehicle_interest: VehicleInterest = VehicleInterest()
    affinity_groups: list[str] = []
    purchase_timeline: str | None = None
    has_trade_in: bool = False
    consent_text: str = Field(..., min_length=10)
    consent_page_url: str = Field(default="")
    trustedform_cert_url: str | None = None


class IncentiveSummary(CamelModel):
    id: str
    name: str
    type: str
    amount: float


class LeadSubmissionResponse(CamelModel):
    lead_id: str
    score: int = 0
    tier: str = "unqualified"
    matched_incentives: list[IncentiveSummary] = []
    total_savings_estimate: float = 0
    matched_dealer_count: int = 0


class LeadDetailResponse(CamelModel):
    lead_id: str
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    zip_code: str
    score: int
    tier: str
    status: str = "new"
    matched_incentives: list[IncentiveSummary] = []
    total_savings_estimate: float = 0
    matched_dealer_count: int = 0
    created_at: str


class LeadStatusUpdate(CamelModel):
    status: str = Field(..., pattern=r"^(new|contacted|converted|nurture|bad_lead)$")


class DealerLeadResponse(CamelModel):
    lead_id: str
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    zip_code: str
    score: int
    tier: str
    total_savings_estimate: float
    vehicle_interest: dict = {}
    created_at: str


class DealerLeadListResponse(CamelModel):
    leads: list[DealerLeadResponse] = []
    total: int = 0


class DealerAnalyticsResponse(CamelModel):
    total_leads: int = 0
    hot_leads: int = 0
    warm_leads: int = 0
    nurture_leads: int = 0
    avg_score: float = 0
    avg_response_time_minutes: float | None = None
