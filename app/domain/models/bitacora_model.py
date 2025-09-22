from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.domain._base.base_model import BaseModel


class Bitacora(BaseModel):
    __tablename__ = "bitacora"

    usuario_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("usuario.id"), nullable=True
    )

    pr_vida: Mapped[bool] = mapped_column(default=False, nullable=False)
    pr_embeddings: Mapped[bool] = mapped_column(default=False, nullable=False)
    pr_landmarks: Mapped[bool] = mapped_column(default=False, nullable=False)

    duracion_total: Mapped[Optional[float]] = mapped_column(nullable=True)
    duracion_spoofing: Mapped[Optional[float]] = mapped_column(nullable=True)
    duracion_identificacion: Mapped[Optional[float]] = mapped_column(nullable=True)

    path: Mapped[Optional[str]] = mapped_column(
        nullable=True
    )  # ruta del frame guardado si corresponde

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="bitacoras")
