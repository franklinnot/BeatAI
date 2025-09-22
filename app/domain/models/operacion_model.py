from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.domain._base.base_model import BaseModel


class Operacion(BaseModel):
    __tablename__ = "operacion"

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    total_muestras: Mapped[int] = mapped_column(default=0, nullable=False)
    duracion: Mapped[Optional[float]] = mapped_column(nullable=True)

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="operaciones")
    muestras: Mapped[List["Muestra"]] = relationship(
        "Muestra", back_populates="operacion", cascade="all, delete-orphan"
    )
