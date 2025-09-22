from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.domain._base.base_model import BaseModel


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
