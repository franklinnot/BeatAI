from typing import Optional, List
from sqlalchemy.orm import Session

#
from app.application.utils.get_muestras import get_muestras
from app.domain.models import Muestra
from app.domain.repositories.muestra_repository import muestra_repository


def register_muestras(
    db: Session,
    operacion_id: int,
    camera_index: int = 0,
    duration_capture: int = 4,
    show_preview: bool = False,
) -> int | None:

    muestras_count = 0
    samples: Optional[List[Muestra]] = get_muestras(
        camera_index, duration_capture, show_preview
    )
    print(samples)

    if not samples:
        print("No se pudo obtener las muestras.")
        return None

    muestras_count = len(samples)
    # Guardar las muestras en la base de datos
    for sample in samples:
        sample.operacion_id = operacion_id
        muestra_repository.create(db, obj_in=sample)

    return muestras_count
