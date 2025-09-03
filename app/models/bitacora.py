# app/models/bitacora.py
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from ._manager import Base, db
from datetime import datetime
from typing import Optional  # Importar Optional


class Bitacora(Base):
    __tablename__ = "bitacora"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )

    pr_liveness: Mapped[Optional[bool]] = mapped_column(nullable=True)
    pr_descriptor: Mapped[Optional[bool]] = mapped_column(nullable=True)
    pr_geometry: Mapped[Optional[bool]] = mapped_column(nullable=True)
    status: Mapped[Optional[bool]] = mapped_column(nullable=True)
    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def save(self):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
