import concurrent.futures
from typing import List
import numpy as np
import cv2
import threading
import time
from sqlalchemy.orm import Session
from app.application.utils.capture_frames import capture_frames
from app.domain.models import Usuario
from app.domain.repositories.usuario_repository import usuario_repository
from app.application.utils.get_emb_land import get_emb_land
from app.application.use_cases.identificacion.validar_embedding import validar_embedding
from app.application.use_cases.identificacion.validar_landmarks import validar_landmarks
from app.application.use_cases.identificacion.types.validacion_identidad_class import (
    ValidacionIdentidad,
)


def _validar_identificacion_frame(
    frame: np.ndarray, users_with_samples: List[Usuario], stop_event: threading.Event
) -> ValidacionIdentidad:
    """
    Procesa un frame para la identificación facial, ejecutando la validación
    de embeddings y landmarks en paralelo.
    """
    # CHEQUEO INICIAL: Si la bandera ya está levantada, no hacer nada.
    if stop_event.is_set():
        return ValidacionIdentidad(success=False)

    facial_data = get_emb_land(frame)
    if not facial_data:
        return ValidacionIdentidad(success=False)

    current_embedding, current_landmarks = facial_data

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_embedding = executor.submit(
            validar_embedding, current_embedding, users_with_samples
        )
        future_landmarks = executor.submit(
            validar_landmarks, current_landmarks, users_with_samples
        )
        futures = [future_embedding, future_landmarks]

        # as_completed nos dará el resultado de la tarea que termine primero
        for future in concurrent.futures.as_completed(futures):
            # CHEQUEO INTERMEDIO: Revisar la bandera de nuevo por si se activó mientras esperábamos
            if stop_event.is_set():
                # Cancelar la otra subtarea local antes de salir
                for f in futures:
                    f.cancel()
                return ValidacionIdentidad(success=False)

            user_id = future.result()

            # Si se encontró un ID de usuario
            if user_id:
                # Determinamos qué método fue el exitoso
                es_por_embedding = future == future_embedding
                es_por_landmarks = future == future_landmarks

                # Cancelamos la otra tarea si aún no ha terminado (buena práctica)
                for f in futures:
                    f.cancel()

                # Retornamos inmediatamente el objeto de validación exitoso
                return ValidacionIdentidad(
                    success=True,
                    user_id=user_id,
                    pr_embedding=es_por_embedding,
                    pr_landmarks=es_por_landmarks,
                )

    # Si el bucle termina y no se retornó nada, significa que ambas tareas
    # fallaron (devolvieron None).
    return ValidacionIdentidad(success=False)


def run_identity_phase(
    db: Session,
    cap: cv2.VideoCapture,
    camera_index: int,
    show_preview: bool,
    duration_cap_identity: int = 5,
) -> ValidacionIdentidad:
    """Ejecuta la fase de identificación facial en paralelo."""
    print(
        f"\n--- FASE 2: IDENTIFICACIÓN FACIAL (Capturando por {duration_cap_identity}s) ---"
    )
    print("Mire fijamente a la cámara...")
    time.sleep(2)

    # capturar todos los frames
    frames = capture_frames(
        camera_index,
        duration=duration_cap_identity,
        show_preview=show_preview,
        cap_instance=cap,
    )
    if not frames:
        print("❌ No se pudieron capturar frames para la identificación.")
        return ValidacionIdentidad(success=False)

    users_with_samples = usuario_repository.get_all_with_samples(db)
    # 1. Crear el evento de "freno de emergencia"
    identificacion_exitosa_event = threading.Event()
    start_time_identity = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(
                _validar_identificacion_frame,
                frame,
                users_with_samples,
                identificacion_exitosa_event,
            )
            for frame in frames
        }

        for future in concurrent.futures.as_completed(futures):
            result = future.result()

            if result.success and not identificacion_exitosa_event.is_set():
                # Señalar a todos los demás hilos que paren.
                identificacion_exitosa_event.set()

                duration = round(time.time() - start_time_identity, 2)

                metodo_exitoso = "Embedding" if result.pr_embedding else "Landmarks"
                print(f"✅ Coincidencia exitosa (ID: {result.user_id}) por método: {metodo_exitoso}")            
                print(f"✅ Identificación SUPERADA en {duration}s.")

                for f in futures:
                    f.cancel()

                return ValidacionIdentidad(
                    success=result.success,
                    duration=duration,
                    user_id=result.user_id,
                    pr_embedding=result.pr_embedding,
                    pr_landmarks=result.pr_landmarks,
                )

    print("❌ Falló la identificación facial.")
    return ValidacionIdentidad(success=False)
