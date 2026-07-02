import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Boolean, DateTime, Integer, Index
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class VehicleCatalog(Base):
    __tablename__ = "vehicle_catalog"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    make: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    fuel_types: Mapped[List[str]] = mapped_column(ARRAY(String(10)), default=list)
    body_style: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    source: Mapped[str] = mapped_column(String(50), default="marketcheck")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_vehicle_catalog_make", "make"),
        Index("ix_vehicle_catalog_make_year", "make", "year"),
        Index("ix_vehicle_catalog_active", "is_active"),
    )
