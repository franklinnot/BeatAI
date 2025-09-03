# app/models/muestra.py
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ._manager import Base, db


class Muestra(Base):
    __tablename__ = "muestras"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)

    embedding: Mapped[list[float]] = mapped_column(JSON, nullable=False)
    landmarks: Mapped[dict] = mapped_column(JSON, nullable=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="muestras") # type: ignore

    def save(self):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
