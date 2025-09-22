from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.domain._base.base_model import BaseModel
from typing import List, Optional, Any
from sqlalchemy import ForeignKey, JSON


class Usuario(BaseModel):
    __tablename__ = "usuario"

    dni: Mapped[str] = mapped_column(nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)

    # relaciones
    operaciones: Mapped[List["Operacion"]] = relationship(
        "Operacion", back_populates="usuario", cascade="all, delete-orphan"
    )

    bitacoras: Mapped[List["Bitacora"]] = relationship(
        "Bitacora", back_populates="usuario", cascade="all, delete-orphan"
    )


class Operacion(BaseModel):
    __tablename__ = "operacion"

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    total_muestras: Mapped[int] = mapped_column(default=0, nullable=False)
    duracion: Mapped[Optional[float]] = mapped_column(nullable=True)

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="operaciones")
    muestras: Mapped[List["Muestra"]] = relationship(
        "Muestra", back_populates="operacion", cascade="all, delete-orphan"
    )


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
