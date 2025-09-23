from typing import Optional
from sqlalchemy.orm import Session, joinedload
from app.domain._base.base_repository import BaseRepository
from app.domain.models import Usuario, Operacion
from typing import List


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self):
        super().__init__(Usuario)

    def get_by_dni(self, db: Session, *, dni: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.dni == dni).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.email == email).first()

    def get_all_with_samples(self, db: Session) -> List[Usuario]:
        """
        Obtiene todos los usuarios con sus operaciones y muestras precargadas
        para evitar consultas N+1. Esencial para el proceso de identificación.
        """
        return (
            db.query(Usuario)
            .options(joinedload(Usuario.operaciones).joinedload(Operacion.muestras))
            .all()
        )


# instancia lista para uso en la app
usuario_repository = UsuarioRepository()
