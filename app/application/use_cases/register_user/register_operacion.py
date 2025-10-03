import time
from sqlalchemy.orm import Session
from typing import Optional
from app.domain.repositories.operacion_repository import operacion_repository
from app.domain.models import Operacion
from app.application.use_cases.register_user.register_muestras import register_muestras
from typing import Optional
from app.domain.classes import OperacionResultado


def register_operacion(
    db: Session,
    usuario_id: int,
    camera_index: int = 0,
    duration_capture: int = 4,
    show_preview: bool = False,
) -> Optional[OperacionResultado]:

    created_operation = operacion_repository.create(
        db, obj_in=Operacion(usuario_id=usuario_id)
    )
    print(f"Operación de registro creada con ID: {created_operation.id}")

    start_time = time.time()
    muestras_count = (
        register_muestras(
            db=db,
            operacion_id=created_operation.id,
            camera_index=camera_index,
            duration_capture=duration_capture,
            show_preview=show_preview,
        )
        or 0
    )

    total_duration = round(time.time() - start_time, 2)

    operacion_repository.update(
        db=db,
        db_obj=created_operation,
        obj_in={"total_muestras": muestras_count, "duracion": total_duration},
    )
    print(
        f"\nProceso de registro finalizado. Se guardaron {muestras_count} muestras en {total_duration} segundos."
    )
    return OperacionResultado(
        id=created_operation.id,
        total_muestras=muestras_count,
        duracion=total_duration,
    )
