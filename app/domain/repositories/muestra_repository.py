from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.domain._base.base_repository import BaseRepository
from app.domain.models.muestra_model import Muestra


class MuestraRepository(BaseRepository[Muestra]):
    def __init__(self):
        super().__init__(Muestra)

    def get_by_operacion(
        self, db: Session, *, operacion_id: int, skip: int = 0, limit: int = 100
    ) -> List[Muestra]:
        return (
            db.query(Muestra)
            .filter(Muestra.operacion_id == operacion_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


muestra_repository = MuestraRepository()
