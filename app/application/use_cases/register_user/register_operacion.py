import time
from sqlalchemy.orm import Session
from typing import Optional
from app.domain.repositories.usuario_repository import usuario_repository
from app.domain.repositories.operacion_repository import operacion_repository
from app.domain.models.usuario_model import Usuario
from app.domain.models.operacion_model import Operacion
from app.application.use_cases.register_user.register_muestras import register_muestras


def register_operacion(
    db: Session,
    *,
    usuario_id: int,
    camera_index: int = 0,
    duration: int = 4,
) -> Optional[Operacion]:

    new_operation = Operacion(usuario_id=usuario_id)
    created_operation = operacion_repository.create(db, obj_in=new_operation)
    print(f"Operación de registro creada con ID: {created_operation.id}")

    start_time = time.time()
    muestras_count = register_muestras(
        db,
        operacion_id=created_operation.id,
        camera_index=camera_index,
        duration=duration,
        # cambiar a True para ver una ventana de previsualización
        show_preview=False,
    )

    end_time = time.time()
    total_duration = end_time - start_time

    operacion_repository.update(
        db,
        db_obj=created_operation,
        obj_in={"total_muestras": muestras_count, "duracion": total_duration},
    )
    print(
        f"\nProceso de registro finalizado. Se guardaron {muestras_count} muestras en {total_duration:.2f} segundos."
    )

    return new_operation
