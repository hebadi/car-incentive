import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Float, Integer, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class LeadDealerMatch(Base):
    __tablename__ = "lead_dealer_matches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    dealer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("dealers.id", ondelete="CASCADE"), nullable=False)

    distance_miles: Mapped[float] = mapped_column(Float, nullable=False)
    match_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_exclusive: Mapped[bool] = mapped_column(Boolean, default=False)
    accepted: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_lead_dealer_matches_lead_id", "lead_id"),
        Index("ix_lead_dealer_matches_dealer_id", "dealer_id"),
    )
