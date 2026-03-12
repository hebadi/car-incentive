"""
Database migration script for lead capture and dealer delivery tables.

Creates all enum types and tables needed for the lead/dealer system.
Uses a sync engine (psycopg2) since this is a one-off migration script.
"""

import sys
import os

# Add the project root to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text

# Import Base and all models to register them with metadata
from app.database import Base
from app.models.incentive_program import IncentiveProgram
from app.models.lead import Lead
from app.models.dealer import Dealer
from app.models.consent_record import ConsentRecord
from app.models.lead_delivery import LeadDelivery
from app.models.lead_dealer_match import LeadDealerMatch

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/incentive_drive"

ENUM_TYPES = [
    ("lead_tier_enum", ["hot", "warm", "nurture", "unqualified"]),
    ("dealer_subscription_tier_enum", ["starter", "growth", "enterprise"]),
    ("consent_method_enum", ["web_form", "api"]),
    ("delivery_method_enum", ["adf_email", "crm_api", "email_plain"]),
    ("delivery_status_enum", ["pending", "sent", "delivered", "failed", "bounced"]),
]

TABLES_TO_CREATE = [
    "leads",
    "dealers",
    "consent_records",
    "lead_deliveries",
    "lead_dealer_matches",
]


def create_enum_types(engine):
    """Create PostgreSQL enum types if they don't already exist."""
    with engine.connect() as conn:
        for enum_name, values in ENUM_TYPES:
            # Check if enum type already exists
            result = conn.execute(
                text("SELECT 1 FROM pg_type WHERE typname = :name"),
                {"name": enum_name},
            )
            if result.fetchone():
                print(f"  Enum '{enum_name}' already exists, skipping.")
            else:
                values_str = ", ".join(f"'{v}'" for v in values)
                conn.execute(text(f"CREATE TYPE {enum_name} AS ENUM ({values_str})"))
                print(f"  Created enum '{enum_name}' with values: {values}")
        conn.commit()


def create_tables(engine):
    """Create all tables using SQLAlchemy metadata."""
    for table_name in TABLES_TO_CREATE:
        table = Base.metadata.tables.get(table_name)
        if table is not None:
            table.create(engine, checkfirst=True)
            print(f"  Created table '{table_name}' (if not exists).")
        else:
            print(f"  WARNING: Table '{table_name}' not found in metadata.")


def main():
    print("IncentiveDrive - Lead & Dealer Migration")
    print("=" * 45)
    print(f"Database: {DATABASE_URL}")
    print()

    engine = create_engine(DATABASE_URL, echo=False)

    print("Step 1: Creating enum types...")
    create_enum_types(engine)
    print()

    print("Step 2: Creating tables...")
    create_tables(engine)
    print()

    print("Migration complete!")
    engine.dispose()


if __name__ == "__main__":
    main()
