from typing import List
from sqlalchemy.orm import Session
from app.domain._base_repository import BaseRepository
from app.domain.models import Operacion


class OperacionRepository(BaseRepository[Operacion]):
    def __init__(self):
        super().__init__(Operacion)

    def get_by_usuario(
        self, db: Session, usuario_id: int, skip: int = 0, limit: int = 100
    ) -> List[Operacion]:
        return (
            db.query(Operacion)
            .filter(Operacion.usuario_id == usuario_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


operacion_repository = OperacionRepository()
