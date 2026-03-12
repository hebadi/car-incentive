from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


def _to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(w.capitalize() for w in parts[1:])


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=_to_camel, populate_by_name=True, serialize_by_alias=True)


class VehicleInterest(CamelModel):
    make: str | None = None
    model: str | None = None
    year: int | None = Field(None, ge=1990, le=2030)
    fuel_type: str | None = Field(None, pattern=r"^(BEV|PHEV|FCEV|ICE|HEV)$")
    new_or_used: str | None = Field(None, pattern=r"^(new|used)$")
    msrp: float | None = Field(None, ge=0, le=500_000)


class BuyerProfile(CamelModel):
    income_range: str | None = None
    filing_status: str | None = Field(None, pattern=r"^(single|married_joint|married_separate|married_filing_jointly|head_of_household)$")
    affinity_groups: list[str] = []
    has_trade_in: bool = False


class CalculateIncentivesRequest(CamelModel):
    zip_code: str = Field(..., min_length=5, max_length=10, pattern=r"^\d{5}(-\d{4})?$")
    vehicle_interest: VehicleInterest = VehicleInterest()
    buyer_profile: BuyerProfile = BuyerProfile()


class ClaimStep(CamelModel):
    step: int
    title: str
    description: str
    documents: list[str] = []
    url: str | None = None


class IncentiveSummary(CamelModel):
    id: str
    name: str
    type: str
    amount: float
    claim_mechanism: str
    confidence_score: float
    source_url: str | None = None
    funding_status: str | None = None
    end_date: str | None = None
    last_verified: str | None = None
    eligible_purchase_types: list[str] = ["cash", "finance", "lease"]
    claim_steps: list[ClaimStep] = []


class CalculateIncentivesResponse(CamelModel):
    incentives: list[IncentiveSummary] = []
    total_savings: float = 0
    confidence: float = 0
    disclaimers: list[str] = []


class IncentiveProgramResponse(CamelModel):
    id: str
    name: str
    type: str
    source_authority: str
    geographic_scope: str
    incentive_value_type: str
    incentive_amount: float | None = None
    incentive_max_amount: float | None = None
    incentive_percentage: float | None = None
    funding_status: str
    claim_mechanism: str
    confidence_score: float
    start_date: str
    end_date: str | None = None
    source_url: str


class IncentiveListResponse(CamelModel):
    incentives: list[IncentiveProgramResponse] = []
    total: int = 0
