import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as PgEnum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class LeadDelivery(Base):
    __tablename__ = "lead_deliveries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    dealer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("dealers.id", ondelete="CASCADE"), nullable=False)

    delivery_method: Mapped[str] = mapped_column(
        PgEnum("adf_email", "crm_api", "email_plain", name="delivery_method_enum", create_type=False),
        nullable=False,
        default="adf_email",
    )
    status: Mapped[str] = mapped_column(
        PgEnum("pending", "sent", "delivered", "failed", "bounced", name="delivery_status_enum", create_type=False),
        nullable=False,
        default="pending",
    )

    adf_xml: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    delivery_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(default=0)

    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    delivered_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_lead_deliveries_lead_id", "lead_id"),
        Index("ix_lead_deliveries_dealer_id", "dealer_id"),
        Index("ix_lead_deliveries_status", "status"),
    )
