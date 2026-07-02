from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


def _to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(w.capitalize() for w in parts[1:])


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=_to_camel,
        populate_by_name=True,
        serialize_by_alias=True,
    )


class VehicleModelInfo(CamelModel):
    name: str
    fuel_types: List[str]


class VehicleModelsResponse(CamelModel):
    make: str
    models: List[VehicleModelInfo]
    source: str = "database"


class VehicleMakesResponse(CamelModel):
    makes: List[str]
    source: str = "database"
