from sqlalchemy.orm import Session
from typing import Tuple, Optional

#
from app.domain.repositories.bitacora_repository import bitacora_repository
from app.application.use_cases.identificacion.validar_identidad.validar_identificacion import (
    run_identity_phase,
)
from app.domain.enums import Estado
from app.domain.classes import BitacoraTemporal
from app.application.use_cases.identificacion.classes import ValidacionIdentidad


def exec_identificacion(
    db: Session, bitacora_temp: BitacoraTemporal, camera_index: int = 0
) -> ValidacionIdentidad:
    result = run_identity_phase(
        db=db,
        show_preview=False,
        camera_index=camera_index,
        duration_capture=3,
        from_terminal=False,
    )

    bitacora = bitacora_repository.get_by_id(db, bitacora_temp.id)
    if not bitacora:
        print(f"[WARN] Bitácora con ID {bitacora_temp.id} no encontrada.")
        return result

    bitacora_repository.update(
        db=db,
        db_obj=bitacora,
        obj_in={
            "usuario_id": result.user_id,
            "pr_embeddings": result.pr_embedding,
            "pr_landmarks": result.pr_landmarks,
            "duracion_total": round(
                (bitacora_temp.duracion_total or 0.0) + (result.duration or 0.0), 2
            ),
            "duracion_identificacion": result.duration,
            "estado": Estado.HABILITADO if result.success else Estado.DESHABILITADO,
        },
    )

    return result
