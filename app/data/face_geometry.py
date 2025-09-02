from sqlalchemy import Column, Integer, ForeignKey, JSON
from .database import Base, db


class FaceGeometry(Base):
    __tablename__ = "face_geometry"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    geometry_data = Column(JSON, nullable=False)  # Ej: proporciones faciales

    def save(self):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
