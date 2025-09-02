from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base, db


class Bitacora(Base):
    __tablename__ = "bitacora"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    usuario = relationship("Usuario", back_populates="bitacora_records")

    def __repr__(self) -> str:
        return f"<Bitacora(id={self.id}, usuario_id={self.usuario_id})>"

    def save(self):
        db.add(self)
        db.commit()
        db.refresh(self)

    def delete(self):
        db.delete(self)
        db.commit()

    @classmethod
    def find(cls, **kwargs):
        return db.query(cls).filter_by(**kwargs).first()

    @classmethod
    def all(cls):
        return db.query(cls).all()

    @classmethod
    def find_latest_by_usuario(cls, usuario_id: int):
        return (
            db.query(cls)
            .filter(cls.usuario_id == usuario_id)
            .order_by(cls.created_at.desc())
            .first()
        )
