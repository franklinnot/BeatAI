from typing import Optional, List
from app.application.utils.get_muestras import get_muestras
from app.domain.models import Muestra
from app.domain.repositories.muestra_repository import muestra_repository
from sqlalchemy.orm import Session


def register_muestras(
    db: Session,
    operacion_id: int,
    camera_index: int = 0,
    duration: int = 4,
    show_preview: bool = False,
) -> int | None:
    """
    Obtiene muestras faciales y los guarda en la base de datos.

    Args:
        db: Sesión de la base de datos.
        operacion_id: ID de la operación a la que se asociarán las muestras.
        camera_index: Índice de la cámara a usar.
        duration: Duración de la captura en segundos.
        show_preview: Si es True, muestra una ventana de vista previa.

    Returns:
        El número de muestras capturadas.
    """

    muestras_count = 0
    samples: Optional[List[Muestra]] = get_muestras(camera_index, duration, show_preview)
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
