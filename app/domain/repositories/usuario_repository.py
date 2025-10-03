from typing import Optional
from sqlalchemy.orm import Session, contains_eager
from app.domain._base_repository import BaseRepository
from app.domain.models import Usuario, Operacion, Muestra
from typing import List
from app.domain.enums import Estado


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self):
        super().__init__(Usuario)

    def get_by_dni(self, db: Session, dni: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.dni == dni).first()

    def get_by_email(self, db: Session, email: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.email == email).first()

    def get_all_with_samples(self, db: Session) -> List[Usuario]:
        """
        Obtiene solo usuarios HABILITADOS con operaciones y muestras HABILITADAS.
        """
        query = (
            db.query(Usuario)
            .join(Usuario.operaciones)  # JOIN con operaciones
            .join(Operacion.muestras)  # JOIN con muestras
            .filter(
                Usuario.estado == Estado.HABILITADO,
                Operacion.estado == Estado.HABILITADO,
                Muestra.estado == Estado.HABILITADO,
            )
            .options(
                contains_eager(Usuario.operaciones).contains_eager(Operacion.muestras)
            )
        )
        return query.all()


# instancia lista para uso en la app
usuario_repository = UsuarioRepository()
