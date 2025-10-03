from sqlalchemy.orm import Session
from app.domain._base_repository import BaseRepository
from app.domain.models import Bitacora


class BitacoraRepository(BaseRepository[Bitacora]):
    def __init__(self):
        super().__init__(Bitacora)

    def create_log(self, db: Session, log: Bitacora) -> Bitacora:
        return self.create(db=db, obj_in=log)


bitacora_repository = BitacoraRepository()
