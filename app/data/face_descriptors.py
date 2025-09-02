from sqlalchemy import Column, Integer, ForeignKey, JSON
from .database import Base, db


class FaceDescriptor(Base):
    __tablename__ = "face_descriptors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    descriptor_data = Column(JSON, nullable=False)  # Ej: vector de embedding facial

    def save(self):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
