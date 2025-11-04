from typing import Tuple
from sqlalchemy.orm import Session

#
from app.domain.models import Bitacora
from app.domain.repositories.bitacora_repository import bitacora_repository
from app.application.use_cases.identificacion.validar_prueba_vida import (
    run_liveness_phase,
)
from app.domain.enums import Estado
from app.domain.classes import BitacoraTemporal
from app.application.use_cases.identificacion.classes import ValidacionVida

# registrar en la bitacora


def exec_prueba_vida(
    db: Session, cantidad_dedos: int, camera_index: int = 0
) -> Tuple[BitacoraTemporal, ValidacionVida]:
    result = run_liveness_phase(
        cantidad_dedos_reto=cantidad_dedos,
        show_preview=False,
        camera_index=camera_index,
        duration_capture=3,
        from_terminal=False,
    )

    bitacora = Bitacora(
        pr_vida=result.success,
        duracion_total=result.duration,
        duracion_spoofing=result.duration,
        estado=Estado.DESHABILITADO,
    )

    bitacora = bitacora_repository.create(db, obj_in=bitacora)

    # Crear un objeto liviano para pasar a la siguiente fase
    bitacora_temp = BitacoraTemporal(
        id=bitacora.id,
        pr_vida=bitacora.pr_vida,
        duracion_total=bitacora.duracion_total or 0,
        duracion_spoofing=bitacora.duracion_spoofing or 0,
        created_at=bitacora.created_at.strftime("%H:%M:%S"),
    )

    return bitacora_temp, result
