import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Integer, Numeric, Boolean, DateTime, Enum as PgEnum, Index
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    zip_code: Mapped[str] = mapped_column(String(10), nullable=False)
    full_address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    income_range: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Vehicle interest
    vehicle_interest: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Affinity groups
    affinity_groups: Mapped[List[str]] = mapped_column(ARRAY(String(50)), default=list)

    purchase_timeline: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    has_trade_in: Mapped[bool] = mapped_column(Boolean, default=False)

    # Scoring
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tier: Mapped[str] = mapped_column(
        PgEnum("hot", "warm", "nurture", "unqualified", name="lead_tier_enum", create_type=False),
        nullable=False,
        default="unqualified",
    )

    # Incentive match results
    matched_incentive_ids: Mapped[List[str]] = mapped_column(ARRAY(UUID(as_uuid=True)), default=list)
    total_savings_estimate: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    # Lead status
    status: Mapped[str] = mapped_column(
        PgEnum("new", "contacted", "converted", "nurture", "bad_lead", name="lead_status_enum", create_type=False),
        nullable=False,
        default="new",
    )

    # Tracking
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="web")
    source_ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_leads_zip_code", "zip_code"),
        Index("ix_leads_tier", "tier"),
        Index("ix_leads_score", "score"),
        Index("ix_leads_created_at", "created_at"),
        Index("ix_leads_email", "email"),
    )
