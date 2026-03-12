from __future__ import annotations
"""
Seed script for dealer data.

Populates the dealers table with sample dealers across key EV-incentive markets
for testing lead capture and delivery.

Usage:
    python -m scripts.seed_dealers
    DATABASE_URL=postgres://... python -m scripts.seed_dealers
"""

import asyncio
import os
import uuid
from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/incentive_drive",
)

NOW = datetime.now(timezone.utc)


def _id(name: str) -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_DNS, name)


def _dealer(
    name: str,
    *,
    contact_email: str,
    phone: str,
    address: str,
    city: str,
    state: str,
    zip_code: str,
    latitude: float,
    longitude: float,
    makes: list[str],
    subscription_tier: str = "starter",
    max_leads_per_day: int = 50,
    min_lead_score: int = 20,
    radius_miles: int = 25,
    vehicle_type_preferences: list[str] | None = None,
    exclusive_leads: bool = False,
    monthly_budget: float = 2000.00,
) -> dict:
    slug = name.lower().replace(" ", "").replace("'", "")
    return {
        "id": _id(name),
        "name": name,
        "contact_email": contact_email,
        "crm_email": f"leads@{slug}.com",
        "phone": phone,
        "address": address,
        "city": city,
        "state": state,
        "zip_code": zip_code,
        "latitude": latitude,
        "longitude": longitude,
        "makes": makes,
        "subscription_tier": subscription_tier,
        "max_leads_per_day": max_leads_per_day,
        "min_lead_score": min_lead_score,
        "radius_miles": radius_miles,
        "vehicle_type_preferences": vehicle_type_preferences or [],
        "exclusive_leads": exclusive_leads,
        "monthly_budget": monthly_budget,
        "budget_spent_this_month": 0,
        "is_active": True,
        "created_at": NOW,
        "updated_at": NOW,
    }


# ---------------------------------------------------------------------------
# Dealer data across key EV-incentive markets
# ---------------------------------------------------------------------------

ALL_DEALERS = [
    # --- California (5) ---
    _dealer(
        "Bay Area Hyundai",
        contact_email="manager@bayareahyundai.com",
        phone="415-555-0101",
        address="1200 Van Ness Ave",
        city="San Francisco",
        state="CA",
        zip_code="94109",
        latitude=37.7870,
        longitude=-122.4215,
        makes=["Hyundai", "Genesis"],
        subscription_tier="growth",
        max_leads_per_day=40,
        min_lead_score=25,
        radius_miles=30,
        vehicle_type_preferences=["SUV", "Sedan"],
        monthly_budget=3500.00,
    ),
    _dealer(
        "SoCal Toyota",
        contact_email="sales@socaltoyota.com",
        phone="213-555-0102",
        address="5400 Wilshire Blvd",
        city="Los Angeles",
        state="CA",
        zip_code="90036",
        latitude=34.0622,
        longitude=-118.3437,
        makes=["Toyota", "Lexus"],
        subscription_tier="growth",
        max_leads_per_day=50,
        min_lead_score=20,
        radius_miles=35,
        vehicle_type_preferences=["SUV", "Truck", "Sedan"],
        monthly_budget=4000.00,
    ),
    _dealer(
        "San Diego Chevrolet",
        contact_email="info@sdchevrolet.com",
        phone="619-555-0103",
        address="3020 National City Blvd",
        city="San Diego",
        state="CA",
        zip_code="91950",
        latitude=32.6695,
        longitude=-117.0988,
        makes=["Chevrolet", "GMC", "Buick"],
        subscription_tier="starter",
        max_leads_per_day=30,
        min_lead_score=30,
        radius_miles=25,
        vehicle_type_preferences=["Truck", "SUV"],
        monthly_budget=2000.00,
    ),
    _dealer(
        "Sacramento Ford",
        contact_email="contact@sacramentoford.com",
        phone="916-555-0104",
        address="2500 Fulton Ave",
        city="Sacramento",
        state="CA",
        zip_code="95825",
        latitude=38.5816,
        longitude=-121.4093,
        makes=["Ford", "Lincoln"],
        subscription_tier="starter",
        max_leads_per_day=35,
        min_lead_score=25,
        radius_miles=40,
        vehicle_type_preferences=["Truck", "SUV", "Sedan"],
        monthly_budget=2500.00,
    ),
    _dealer(
        "Orange County Nissan",
        contact_email="sales@ocnissan.com",
        phone="714-555-0105",
        address="1501 Auto Mall Dr",
        city="Irvine",
        state="CA",
        zip_code="92618",
        latitude=33.6846,
        longitude=-117.8265,
        makes=["Nissan", "Infiniti"],
        subscription_tier="growth",
        max_leads_per_day=45,
        min_lead_score=20,
        radius_miles=30,
        vehicle_type_preferences=["SUV", "Sedan"],
        monthly_budget=3000.00,
    ),
    # --- Colorado (3) ---
    _dealer(
        "Mile High Ford",
        contact_email="team@milehighford.com",
        phone="303-555-0201",
        address="7800 E Colfax Ave",
        city="Denver",
        state="CO",
        zip_code="80220",
        latitude=39.7400,
        longitude=-104.9103,
        makes=["Ford", "Lincoln"],
        subscription_tier="growth",
        max_leads_per_day=40,
        min_lead_score=25,
        radius_miles=35,
        vehicle_type_preferences=["Truck", "SUV"],
        monthly_budget=3000.00,
    ),
    _dealer(
        "Springs Volkswagen",
        contact_email="sales@springsvw.com",
        phone="719-555-0202",
        address="1330 Motor City Dr",
        city="Colorado Springs",
        state="CO",
        zip_code="80905",
        latitude=38.8339,
        longitude=-104.8214,
        makes=["Volkswagen", "Audi"],
        subscription_tier="starter",
        max_leads_per_day=25,
        min_lead_score=30,
        radius_miles=30,
        vehicle_type_preferences=["SUV", "Sedan"],
        monthly_budget=2000.00,
    ),
    _dealer(
        "Boulder Honda",
        contact_email="info@boulderhonda.com",
        phone="303-555-0203",
        address="2750 28th St",
        city="Boulder",
        state="CO",
        zip_code="80301",
        latitude=40.0220,
        longitude=-105.2519,
        makes=["Honda", "Acura"],
        subscription_tier="starter",
        max_leads_per_day=30,
        min_lead_score=25,
        radius_miles=25,
        vehicle_type_preferences=["SUV", "Sedan"],
        monthly_budget=2000.00,
    ),
    # --- New York (3) ---
    _dealer(
        "Manhattan Toyota",
        contact_email="sales@manhattantoyota.com",
        phone="212-555-0301",
        address="630 11th Ave",
        city="New York",
        state="NY",
        zip_code="10036",
        latitude=40.7637,
        longitude=-73.9962,
        makes=["Toyota", "Lexus"],
        subscription_tier="growth",
        max_leads_per_day=50,
        min_lead_score=30,
        radius_miles=25,
        vehicle_type_preferences=["Sedan", "SUV"],
        exclusive_leads=True,
        monthly_budget=5000.00,
    ),
    _dealer(
        "Long Island Kia",
        contact_email="info@likia.com",
        phone="516-555-0302",
        address="3500 Hempstead Tpke",
        city="Levittown",
        state="NY",
        zip_code="11756",
        latitude=40.7240,
        longitude=-73.5143,
        makes=["Kia", "Hyundai"],
        subscription_tier="starter",
        max_leads_per_day=35,
        min_lead_score=20,
        radius_miles=30,
        vehicle_type_preferences=["SUV", "Sedan"],
        monthly_budget=2500.00,
    ),
    _dealer(
        "Westchester BMW",
        contact_email="sales@westchesterbmw.com",
        phone="914-555-0303",
        address="543 Tarrytown Rd",
        city="White Plains",
        state="NY",
        zip_code="10607",
        latitude=41.0534,
        longitude=-73.7855,
        makes=["BMW", "Mini"],
        subscription_tier="growth",
        max_leads_per_day=30,
        min_lead_score=35,
        radius_miles=25,
        vehicle_type_preferences=["SUV", "Sedan"],
        exclusive_leads=True,
        monthly_budget=4000.00,
    ),
    # --- New Jersey (2) ---
    _dealer(
        "Bergen County Subaru",
        contact_email="info@bergensubaru.com",
        phone="201-555-0401",
        address="300 Route 17 South",
        city="Paramus",
        state="NJ",
        zip_code="07652",
        latitude=40.9568,
        longitude=-74.0712,
        makes=["Subaru", "Mazda"],
        subscription_tier="starter",
        max_leads_per_day=30,
        min_lead_score=25,
        radius_miles=25,
        vehicle_type_preferences=["SUV", "Sedan"],
        monthly_budget=2000.00,
    ),
    _dealer(
        "South Jersey Chevrolet",
        contact_email="sales@sjchevrolet.com",
        phone="856-555-0402",
        address="1200 Route 73",
        city="Mount Laurel",
        state="NJ",
        zip_code="08054",
        latitude=39.9539,
        longitude=-74.8919,
        makes=["Chevrolet", "Cadillac"],
        subscription_tier="starter",
        max_leads_per_day=25,
        min_lead_score=20,
        radius_miles=35,
        vehicle_type_preferences=["Truck", "SUV", "Sedan"],
        monthly_budget=2000.00,
    ),
    # --- Illinois (2) ---
    _dealer(
        "Chicago Tesla Hub",
        contact_email="team@chicagoteslahub.com",
        phone="312-555-0501",
        address="1160 N Clark St",
        city="Chicago",
        state="IL",
        zip_code="60610",
        latitude=41.9023,
        longitude=-87.6317,
        makes=["Tesla", "Rivian"],
        subscription_tier="growth",
        max_leads_per_day=45,
        min_lead_score=30,
        radius_miles=30,
        vehicle_type_preferences=["Sedan", "SUV", "Truck"],
        exclusive_leads=True,
        monthly_budget=5000.00,
    ),
    _dealer(
        "Naperville Honda",
        contact_email="sales@napervillehonda.com",
        phone="630-555-0502",
        address="1100 W Ogden Ave",
        city="Naperville",
        state="IL",
        zip_code="60563",
        latitude=41.7731,
        longitude=-88.1484,
        makes=["Honda", "Acura", "Toyota"],
        subscription_tier="starter",
        max_leads_per_day=35,
        min_lead_score=20,
        radius_miles=30,
        vehicle_type_preferences=["SUV", "Sedan"],
        monthly_budget=2500.00,
    ),
]


# ============================================================================
# DB INSERTION
# ============================================================================


async def seed(database_url: str | None = None) -> None:
    url = database_url or DATABASE_URL
    engine = create_async_engine(url, echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        for d in ALL_DEALERS:
            await session.execute(
                text("""
                    INSERT INTO dealers (
                        id, name, contact_email, crm_email, phone,
                        address, city, state, zip_code,
                        latitude, longitude, makes,
                        subscription_tier,
                        max_leads_per_day, min_lead_score, radius_miles,
                        vehicle_type_preferences, exclusive_leads,
                        monthly_budget, budget_spent_this_month,
                        is_active, created_at, updated_at
                    ) VALUES (
                        :id, :name, :contact_email, :crm_email, :phone,
                        :address, :city, :state, :zip_code,
                        :latitude, :longitude, :makes,
                        :subscription_tier,
                        :max_leads_per_day, :min_lead_score, :radius_miles,
                        :vehicle_type_preferences, :exclusive_leads,
                        :monthly_budget, :budget_spent_this_month,
                        :is_active, :created_at, :updated_at
                    )
                    ON CONFLICT (id) DO UPDATE SET
                        name = EXCLUDED.name,
                        contact_email = EXCLUDED.contact_email,
                        crm_email = EXCLUDED.crm_email,
                        phone = EXCLUDED.phone,
                        address = EXCLUDED.address,
                        city = EXCLUDED.city,
                        state = EXCLUDED.state,
                        zip_code = EXCLUDED.zip_code,
                        latitude = EXCLUDED.latitude,
                        longitude = EXCLUDED.longitude,
                        makes = EXCLUDED.makes,
                        subscription_tier = EXCLUDED.subscription_tier,
                        max_leads_per_day = EXCLUDED.max_leads_per_day,
                        min_lead_score = EXCLUDED.min_lead_score,
                        radius_miles = EXCLUDED.radius_miles,
                        vehicle_type_preferences = EXCLUDED.vehicle_type_preferences,
                        exclusive_leads = EXCLUDED.exclusive_leads,
                        monthly_budget = EXCLUDED.monthly_budget,
                        budget_spent_this_month = EXCLUDED.budget_spent_this_month,
                        is_active = EXCLUDED.is_active,
                        updated_at = EXCLUDED.updated_at
                """),
                {
                    "id": str(d["id"]),
                    "name": d["name"],
                    "contact_email": d["contact_email"],
                    "crm_email": d["crm_email"],
                    "phone": d["phone"],
                    "address": d["address"],
                    "city": d["city"],
                    "state": d["state"],
                    "zip_code": d["zip_code"],
                    "latitude": d["latitude"],
                    "longitude": d["longitude"],
                    "makes": d["makes"],
                    "subscription_tier": d["subscription_tier"],
                    "max_leads_per_day": d["max_leads_per_day"],
                    "min_lead_score": d["min_lead_score"],
                    "radius_miles": d["radius_miles"],
                    "vehicle_type_preferences": d["vehicle_type_preferences"],
                    "exclusive_leads": d["exclusive_leads"],
                    "monthly_budget": d["monthly_budget"],
                    "budget_spent_this_month": d["budget_spent_this_month"],
                    "is_active": d["is_active"],
                    "created_at": d["created_at"],
                    "updated_at": d["updated_at"],
                },
            )

        await session.commit()

    await engine.dispose()
    print(f"Seeded {len(ALL_DEALERS)} dealers.")


if __name__ == "__main__":
    asyncio.run(seed())
