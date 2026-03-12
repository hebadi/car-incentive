import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Integer, Float, Boolean, DateTime, Numeric, Enum as PgEnum, Index
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Dealer(Base):
    __tablename__ = "dealers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_email: Mapped[str] = mapped_column(String(255), nullable=False)
    crm_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(2), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(10), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    # Franchise info
    makes: Mapped[List[str]] = mapped_column(ARRAY(String(50)), default=list)

    # Subscription
    subscription_tier: Mapped[str] = mapped_column(
        PgEnum("starter", "growth", "enterprise", name="dealer_subscription_tier_enum", create_type=False),
        nullable=False,
        default="starter",
    )
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    stripe_subscription_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Lead preferences
    max_leads_per_day: Mapped[int] = mapped_column(Integer, default=50)
    min_lead_score: Mapped[int] = mapped_column(Integer, default=20)
    radius_miles: Mapped[int] = mapped_column(Integer, default=25)
    vehicle_type_preferences: Mapped[List[str]] = mapped_column(ARRAY(String(50)), default=list)
    exclusive_leads: Mapped[bool] = mapped_column(Boolean, default=False)

    # CRM config
    crm_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    crm_api_config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Budget tracking
    monthly_budget: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    budget_spent_this_month: Mapped[float] = mapped_column(Numeric(10, 2), default=0)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_dealers_state", "state"),
        Index("ix_dealers_zip_code", "zip_code"),
        Index("ix_dealers_makes", "makes", postgresql_using="gin"),
        Index("ix_dealers_active", "is_active"),
        Index("ix_dealers_subscription_tier", "subscription_tier"),
    )
