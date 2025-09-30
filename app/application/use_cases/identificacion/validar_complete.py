import time
import cv2
from sqlalchemy.orm import Session
from app.domain.models import Bitacora
from app.domain.repositories.bitacora_repository import bitacora_repository
from app.application.use_cases.identificacion.validar_identificacion import (
    run_identity_phase,
)
from app.application.use_cases.identificacion.validar_prueba_vida import (
    run_liveness_phase,
)
from app.application.use_cases.identificacion.types.validacion_vida_class import (
    ValidacionVida,
)
from app.application.use_cases.identificacion.types.validacion_identidad_class import (
    ValidacionIdentidad,
)
from app.enums.estado import Estado


def validar_complete(
    db: Session,
    cantidad_dedos_reto: int,
    camera_index: int = 0,
    show_preview: bool = False,
    duration_cap_liveness: int = 5,
    duration_cap_identity: int = 5,
) -> bool:
    """Orquesta el flujo de validación e identificacion."""
    obj_validacionIdentidad = ValidacionIdentidad(success=False)

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error crítico: No se pudo abrir la cámara.")
        return False

    try:
        # FASE 1
        obj_validacionVida = run_liveness_phase(
            cap, camera_index, cantidad_dedos_reto, show_preview, duration_cap_liveness
        )
        if not obj_validacionVida.success:
            return False

        # FASE 2
        obj_validacionIdentidad: ValidacionIdentidad = run_identity_phase(
            db, cap, camera_index, show_preview, duration_cap_identity
        )

    finally:
        # Limpieza de Recursos y Logging
        cap.release()
        if show_preview:
            cv2.destroyAllWindows()

        duracion_total = (obj_validacionVida.duration or 0) + (
            obj_validacionIdentidad.duration or 0
        )
        duracion_total = round(duracion_total, 2)
        estado = (
            Estado.HABILITADO
            if obj_validacionIdentidad.success and obj_validacionVida.success
            else Estado.DESHABILITADO
        )

        bitacora = Bitacora(
            usuario_id=obj_validacionIdentidad.user_id,
            pr_vida=obj_validacionVida.success,
            pr_embeddings=obj_validacionIdentidad.pr_embedding,
            pr_landmarks=obj_validacionIdentidad.pr_landmarks,
            duracion_total=duracion_total,
            duracion_spoofing=obj_validacionVida.duration,
            duracion_identificacion=obj_validacionIdentidad.duration,
            estado=estado,
        )

        bitacora_repository.create(db, obj_in=bitacora)
        print(f"\n--- FIN DE VALIDACIÓN --- \nResultado guardado en Bitácora.")

    return obj_validacionVida.success and obj_validacionIdentidad.success
