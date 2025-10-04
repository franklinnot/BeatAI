from sqlalchemy.orm import Session

#
from app.domain.models import Bitacora
from app.domain.repositories.bitacora_repository import bitacora_repository
from app.domain.repositories.usuario_repository import usuario_repository
from app.application.use_cases.identificacion.validar_identidad.validar_identificacion import (
    run_identity_phase,
)
from app.application.use_cases.identificacion.notificar import enviar_correo
from app.application.use_cases.identificacion.validar_prueba_vida import (
    run_liveness_phase,
)
from app.application.use_cases.identificacion.classes import (
    ValidacionIdentidad,
    ValidacionVida,
)
from app.domain.enums import Estado


def validar_complete(
    db: Session,
    cantidad_dedos_reto: int,
    camera_index: int = 0,
    show_preview: bool = False,
    duration_cap_liveness: int = 5,
    duration_cap_identity: int = 5,
    from_terminal: bool = False,
) -> bool:
    obj_validacionIdentidad = ValidacionIdentidad(success=False)
    obj_validacionVida = ValidacionVida(success=False)

    try:
        # FASE 1
        obj_validacionVida = run_liveness_phase(
            cantidad_dedos_reto=cantidad_dedos_reto,
            show_preview=show_preview,
            camera_index=camera_index,
            duration_capture=duration_cap_liveness,
            from_terminal=from_terminal,
        )

        if not obj_validacionVida.success:
            return False

        # FASE 2
        obj_validacionIdentidad = run_identity_phase(
            db=db,
            camera_index=camera_index,
            show_preview=show_preview,
            duration_capture=duration_cap_identity,
            from_terminal=from_terminal,
        )

    finally:
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

        new_bitacora = bitacora_repository.create(db, obj_in=bitacora)
        print(f"Resultado guardado en Bitácora.")

        if new_bitacora and new_bitacora.usuario_id:
            usuario = usuario_repository.get_by_id(db, new_bitacora.usuario_id)
            if usuario:
                enviar_correo(
                    nombre=usuario.nombre,
                    email=usuario.email,
                    b64=obj_validacionIdentidad.b64 or "",
                    hora=new_bitacora.created_at.strftime("%H:%M:%S"),
                )

    return obj_validacionVida.success and obj_validacionIdentidad.success
