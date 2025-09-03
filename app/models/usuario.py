# app/models/usuario.py
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from ._manager import Base, db
from .muestra import Muestra


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    dni: Mapped[str] = mapped_column(String(8), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False)

    muestras: Mapped[List["Muestra"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan"
    )

    def save(self):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
