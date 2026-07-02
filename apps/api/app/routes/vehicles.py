"""Vehicle catalog API — dynamic makes/models from database with fallback."""
from __future__ import annotations

import time
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.vehicle_catalog import VehicleCatalog
from app.schemas.vehicles import (
    VehicleMakesResponse,
    VehicleModelInfo,
    VehicleModelsResponse,
)

router = APIRouter()

# ---- Simple in-memory cache (5-minute TTL) ----
_cache: dict = {}
_CACHE_TTL = 300  # seconds


def _cache_get(key: str):
    entry = _cache.get(key)
    if entry and (time.time() - entry["ts"]) < _CACHE_TTL:
        return entry["data"]
    return None


def _cache_set(key: str, data):
    _cache[key] = {"data": data, "ts": time.time()}


# ---- Hardcoded fallback (mirrors frontend constants.ts) ----
_FALLBACK_MAKES = [
    "Acura", "Audi", "BMW", "Buick", "Cadillac", "Chevrolet", "Chrysler",
    "Dodge", "Fiat", "Ford", "Genesis", "GMC", "Honda", "Hyundai",
    "Infiniti", "Jaguar", "Jeep", "Kia", "Land Rover", "Lexus",
    "Lincoln", "Lucid", "Mazda", "Mercedes-Benz", "MINI", "Mitsubishi",
    "Nissan", "Polestar", "Porsche", "Ram", "Rivian", "Subaru",
    "Tesla", "Toyota", "Volkswagen", "Volvo",
]


@router.get("/makes", response_model=VehicleMakesResponse)
async def list_makes(db: AsyncSession = Depends(get_db)):
    """Return all active vehicle makes."""
    cached = _cache_get("makes")
    if cached:
        return cached

    stmt = (
        select(VehicleCatalog.make)
        .where(VehicleCatalog.is_active.is_(True))
        .distinct()
        .order_by(VehicleCatalog.make)
    )
    result = await db.execute(stmt)
    makes = [row[0] for row in result.all()]

    if makes:
        resp = VehicleMakesResponse(makes=makes, source="database")
    else:
        resp = VehicleMakesResponse(makes=_FALLBACK_MAKES, source="fallback")

    _cache_set("makes", resp)
    return resp


@router.get("/models", response_model=VehicleModelsResponse)
async def list_models(
    make: str = Query(..., min_length=1),
    fuel_type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Return active models for a given make, optionally filtered by fuel type."""
    cache_key = f"models:{make}:{fuel_type or ''}"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    stmt = (
        select(VehicleCatalog.model, VehicleCatalog.fuel_types)
        .where(
            VehicleCatalog.is_active.is_(True),
            func.lower(VehicleCatalog.make) == make.lower(),
        )
        .distinct(VehicleCatalog.model)
        .order_by(VehicleCatalog.model)
    )
    result = await db.execute(stmt)
    rows = result.all()

    # Aggregate fuel types across years for same model
    model_fuels: dict[str, set] = {}
    for model_name, fuel_types in rows:
        if model_name not in model_fuels:
            model_fuels[model_name] = set()
        model_fuels[model_name].update(fuel_types or [])

    # Apply fuel_type filter if provided
    models = []
    for model_name, fuels in sorted(model_fuels.items()):
        fuel_list = sorted(fuels)
        if fuel_type and fuel_type not in fuels:
            continue
        models.append(VehicleModelInfo(name=model_name, fuel_types=fuel_list))

    source = "database" if models else "fallback"

    # Fallback: if DB has nothing for this make, return empty (frontend has its own fallback)
    resp = VehicleModelsResponse(make=make, models=models, source=source)
    _cache_set(cache_key, resp)
    return resp
