from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base, db


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relaciones - se usa una cadena de texto para la clase para evitar el error de importación circular
    face_detectors = relationship(
        "FaceDetector", back_populates="usuario", cascade="all, delete-orphan"
    )
    face_features = relationship(
        "FaceFeatures", back_populates="usuario", cascade="all, delete-orphan"
    )
    liveness_records = relationship(
        "Liveness", back_populates="usuario", cascade="all, delete-orphan"
    )
    bitacora_records = relationship(
        "Bitacora", back_populates="usuario", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"

    def save(self):
        db.add(self)
        db.commit()
        db.refresh(self)

    def delete(self):
        db.delete(self)
        db.commit()

    def refresh(self):
        db.refresh(self)

    @classmethod
    def find(cls, **kwargs):
        return db.query(cls).filter_by(**kwargs).first()

    @classmethod
    def all(cls):
        return db.query(cls).all()

    @classmethod
    def search_by_name(cls, name_pattern: str):
        return db.query(cls).filter(cls.nombre.like(f"%{name_pattern}%")).all()
