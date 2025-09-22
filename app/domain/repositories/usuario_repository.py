from typing import Optional
from sqlalchemy.orm import Session
from app.domain._base.base_repository import BaseRepository
from app.domain.models.usuario_model import Usuario


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self):
        super().__init__(Usuario)

    def get_by_dni(self, db: Session, *, dni: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.dni == dni).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.email == email).first()


# instancia lista para uso en la app
usuario_repository = UsuarioRepository()
