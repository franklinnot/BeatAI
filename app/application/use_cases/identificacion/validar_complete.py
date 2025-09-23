import time
import cv2
import concurrent.futures
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, Tuple

from app.domain.models import Bitacora
from app.domain.repositories.usuario_repository import usuario_repository
from app.domain.repositories.bitacora_repository import bitacora_repository
from app.application.utils.capture_frames import capture_frames
from .validar_identificacion import validar_identificacion
from .validar_prueba_vida import validar_prueba_vida


def _run_liveness_phase(
    cap: cv2.VideoCapture,
    camera_index: int,
    cantidad_dedos_reto: int,
    show_preview: bool,
    timeout_liveness: int = 5,
) -> Tuple[bool, Optional[float]]:
    """
    Ejecuta la fase de prueba de vida con la estrategia de 'capturar primero, procesar después'.
    """
    print(f"--- FASE 1: PRUEBA DE VIDA (Capturando por {timeout_liveness}s) ---")
    print(f"RETO: Muestre {cantidad_dedos_reto} dedo(s) a la cámara.")
    start_time_liveness = time.time()

    # 1. Capturar todos los frames primero, como en get_muestras.
    frames = capture_frames(
        camera_index,
        duration=timeout_liveness,
        show_preview=show_preview,
        cap_instance=cap,
    )
    if not frames:
        print("❌ No se pudieron capturar frames para la prueba de vida.")
        return False, None

    # 2. Procesar todos los frames en paralelo.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(validar_prueba_vida, frame, cantidad_dedos_reto)
            for frame in frames
        }

        for future in concurrent.futures.as_completed(futures):
            # Si CUALQUIER frame es válido, la prueba es un éxito.
            if future.result():
                duration = time.time() - start_time_liveness
                print(f"✅ Prueba de Vida SUPERADA en {duration:.2f}s.")
                # Cancelar las tareas restantes para ahorrar recursos.
                for f in futures:
                    f.cancel()
                return True, duration

    print("❌ Falló la prueba de vida en todos los frames capturados.")
    return False, None


def _run_identity_phase(
    db: Session,
    cap: cv2.VideoCapture,
    camera_index: int,
    show_preview: bool,
    timeout_identity: int = 5,
) -> Dict[str, Any]:
    """Ejecuta la fase de identificación facial en paralelo."""
    print(f"\n--- FASE 2: IDENTIFICACIÓN FACIAL (Capturando por {timeout_identity}s) ---")
    print("Mire fijamente a la cámara...")
    time.sleep(0.5)

    frames_para_id = capture_frames(
        camera_index,
        duration=timeout_identity,
        show_preview=show_preview,
        cap_instance=cap,
    )
    if not frames_para_id:
        print("❌ No se pudieron capturar frames para la identificación.")
        return {"passed": False}

    start_time_identity = time.time()
    users_with_samples = usuario_repository.get_all_with_samples(db)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(validar_identificacion, frame, users_with_samples)
            for frame in frames_para_id
        }
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if not result.get("error") and (
                result["embedding_user_id"] or result["landmarks_user_id"]
            ):
                duration = time.time() - start_time_identity
                print(f"✅ Identificación SUPERADA en {duration:.2f}s.")
                for f in futures:
                    f.cancel()
                return {
                    "passed": True,
                    "duration": duration,
                    "user_id": result["embedding_user_id"]
                    or result["landmarks_user_id"],
                    "pr_embedding": bool(result["embedding_user_id"]),
                    "pr_landmarks": bool(result["landmarks_user_id"]),
                }

    print("❌ Falló la identificación facial.")
    return {"passed": False}


def _log_validation_result(db: Session, **kwargs):
    """Crea y guarda la entrada en la bitácora."""
    log_entry = Bitacora(
        usuario_id=kwargs.get("final_user_id"),
        pr_vida=kwargs.get("liveness_passed", False),
        pr_embeddings=kwargs.get("pr_embedding", False),
        pr_landmarks=kwargs.get("pr_landmarks", False),
        duracion_total=kwargs.get("total_duration"),
        duracion_spoofing=kwargs.get("liveness_duration"),
        duracion_identificacion=kwargs.get("identity_duration"),
    )
    bitacora_repository.create(db, obj_in=log_entry)
    print(f"\n--- FIN DE VALIDACIÓN --- \nResultado guardado en Bitácora.")


def validar_complete(
    db: Session,
    cantidad_dedos_reto: int,
    camera_index: int = 0,
    show_preview: bool = False,
    timeout_liveness: int = 5,
    timeout_identity: int = 5,
) -> bool:
    """Orquesta el flujo de validación de forma modular y eficiente."""
    start_time_total = time.time()
    identity_result = {}

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error crítico: No se pudo abrir la cámara.")
        return False

    try:
        # FASE 1
        liveness_passed, liveness_duration = _run_liveness_phase(
            cap, camera_index, cantidad_dedos_reto, show_preview, timeout_liveness
        )
        if not liveness_passed:
            return False

        # FASE 2
        identity_result = _run_identity_phase(
            db, cap, camera_index, show_preview, timeout_identity
        )

    finally:
        # Limpieza de Recursos y Logging
        cap.release()
        if show_preview:
            cv2.destroyAllWindows()

        _log_validation_result(
            db=db,
            liveness_passed=liveness_passed,
            liveness_duration=liveness_duration,
            identity_duration=identity_result.get("duration"),
            final_user_id=identity_result.get("user_id"),
            pr_embedding=identity_result.get("pr_embedding", False),
            pr_landmarks=identity_result.get("pr_landmarks", False),
            total_duration=time.time() - start_time_total,
        )

    return liveness_passed and identity_result.get("passed", False)
