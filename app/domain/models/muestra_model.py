from typing import Optional, List, Any
from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.domain._base.base_model import BaseModel


class Muestra(BaseModel):
    __tablename__ = "muestra"

    operacion_id: Mapped[int] = mapped_column(
        ForeignKey("operacion.id"), nullable=False
    )

    # embeddings y landmarks como JSON serializable (listas/estructuras)
    embedding: Mapped[List[float]] = mapped_column(JSON, nullable=False)
    landmarks: Mapped[Any] = mapped_column(JSON, nullable=False)

    operacion: Mapped["Operacion"] = relationship(
        "Operacion", back_populates="muestras"
    )
