import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Enum as PgEnum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ConsentRecord(Base):
    __tablename__ = "consent_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    dealer_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("dealers.id", ondelete="CASCADE"), nullable=True)
    consent_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consent_ip: Mapped[str] = mapped_column(String(45), nullable=False)
    consent_user_agent: Mapped[str] = mapped_column(String(500), nullable=False)
    consent_page_url: Mapped[str] = mapped_column(String(512), nullable=False)
    consent_language_version: Mapped[str] = mapped_column(String(64), nullable=False)
    consent_method: Mapped[str] = mapped_column(
        PgEnum("web_form", "api", name="consent_method_enum", create_type=False),
        nullable=False,
        default="web_form",
    )
    trustedform_cert_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    revocation_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    revocation_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_consent_records_lead_id", "lead_id"),
        Index("ix_consent_records_dealer_id", "dealer_id"),
        Index("ix_consent_records_timestamp", "consent_timestamp"),
    )
