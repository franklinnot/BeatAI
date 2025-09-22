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

    def find_similar_by_embedding(
        self, db: Session, *, embedding: list, threshold: float = 0.6
    ) -> Optional[Muestra]:
        """
        Placeholder: en SQLite puro no puedes hacer búsqueda vectorial.
        Aquí podrías traer todas las muestras y comparar en Python.
        En producción, mover embeddings a un índice vectorial.
        """
        todas = db.query(Muestra).all()
        # NOTA: implementar comparación en Python (p.ej. cosine similarity)
        return None


muestra_repository = MuestraRepository()
