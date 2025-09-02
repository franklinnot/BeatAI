from sqlalchemy import Column, Integer, String
from .database import Base, db


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def save(self):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
