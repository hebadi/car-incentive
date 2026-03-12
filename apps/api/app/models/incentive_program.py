import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Numeric, Boolean, DateTime, Float, Enum as PgEnum, Index
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class IncentiveProgram(Base):
    __tablename__ = "incentive_programs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(
        PgEnum("federal", "state", "manufacturer", "utility", "affinity", name="incentive_type_enum", create_type=False),
        nullable=False,
    )
    source_authority: Mapped[str] = mapped_column(String(255), nullable=False)
    geographic_scope: Mapped[str] = mapped_column(
        PgEnum("national", "state", "county", "zip", "utility_territory", name="geographic_scope_enum", create_type=False),
        nullable=False,
    )
    eligible_states: Mapped[List[str]] = mapped_column(ARRAY(String(2)), default=list)
    eligible_zips: Mapped[List[str]] = mapped_column(ARRAY(String(10)), default=list)
    eligible_purchase_types: Mapped[List[str]] = mapped_column(ARRAY(String(10)), default=lambda: ["cash", "finance", "lease"])

    # Vehicle criteria (JSONB for flexibility)
    vehicle_criteria: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Buyer criteria
    buyer_criteria: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Incentive value
    incentive_value_type: Mapped[str] = mapped_column(
        PgEnum("fixed", "percentage", "tax_credit", "rate_reduction", name="incentive_value_type_enum", create_type=False),
        nullable=False,
    )
    incentive_amount: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    incentive_max_amount: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    incentive_percentage: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)

    # Stacking rules
    stackable_with: Mapped[List[str]] = mapped_column(ARRAY(UUID(as_uuid=True)), default=list)
    mutually_exclusive_with: Mapped[List[str]] = mapped_column(ARRAY(UUID(as_uuid=True)), default=list)

    # Timing
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    application_deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    funding_status: Mapped[str] = mapped_column(
        PgEnum("open", "waitlisted", "depleted", "suspended", name="funding_status_enum", create_type=False),
        nullable=False,
        default="open",
    )

    claim_mechanism: Mapped[str] = mapped_column(
        PgEnum("point_of_sale", "tax_return", "post_purchase_rebate", "lease_reduction", name="claim_mechanism_enum", create_type=False),
        nullable=False,
    )

    claim_steps: Mapped[list] = mapped_column(JSONB, default=list)

    last_verified: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    source_url: Mapped[str] = mapped_column(String(512), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_incentive_programs_type", "type"),
        Index("ix_incentive_programs_eligible_states", "eligible_states", postgresql_using="gin"),
        Index("ix_incentive_programs_funding_status", "funding_status"),
        Index("ix_incentive_programs_active", "is_active"),
    )
