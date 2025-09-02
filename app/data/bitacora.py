from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base, db


class Bitacora(Base):
    __tablename__ = "bitacora"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)  # opcional
    status = Column(Boolean, default=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())

    def save(self):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
