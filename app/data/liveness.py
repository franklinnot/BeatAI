from sqlalchemy import Column, Integer, Boolean, ForeignKey
from .database import Base, db


class Liveness(Base):
    __tablename__ = "liveness"

    id = Column(Integer, primary_key=True, index=True)
    bitacora_id = Column(Integer, ForeignKey("bitacora.id"), nullable=False)
    es_vivo = Column(Boolean, default=False)

    def save(self):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
