from __future__ import annotations

from pydantic import BaseModel


class DealerSummary(BaseModel):
    id: str
    name: str
    phone: str
    address: str
    city: str
    state: str
    zip_code: str
    makes: list[str] = []
    distance_miles: float | None = None


class DealerSearchResponse(BaseModel):
    dealers: list[DealerSummary] = []
    total: int = 0
