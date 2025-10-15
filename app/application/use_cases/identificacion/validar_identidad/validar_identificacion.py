import concurrent.futures
from typing import List, Optional
import threading
from threading import Event
import time
from sqlalchemy.orm import Session

#
from app.domain.models import Usuario, Muestra
from app.domain.repositories.usuario_repository import usuario_repository
from app.application.utils.get_muestras import get_muestras_with_b64
from app.application.use_cases.identificacion.classes import ValidacionIdentidad
from app.application.use_cases.identificacion.validar_identidad._validar_embedding import (
    validar_embedding,
)
from app.application.use_cases.identificacion.validar_identidad._validar_landmarks import (
    validar_landmarks,
)


def _evaluar_muestra(
    users_with_samples: List[Usuario], muestra: Muestra, stop_event: Event
) -> Optional[ValidacionIdentidad]:
    if stop_event.is_set():
        return None  # Ya se encontró un resultado, no procesar más

    current_embedding = muestra.embedding
    current_landmarks = muestra.landmarks

    # Ejecutar embedding y landmarks en paralelo para esta muestra
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_emb = executor.submit(
            validar_embedding, current_embedding, users_with_samples
        )
        future_lmk = executor.submit(
            validar_landmarks, current_landmarks, users_with_samples
        )

        # Esperar el primero que termine y tenga éxito
        for future in concurrent.futures.as_completed([future_emb, future_lmk]):
            if stop_event.is_set():
                return None  # Ya resuelto por otra muestra
            try:
                user_id = future.result()
                if user_id is not None:
                    # Determinar qué método tuvo éxito
                    if future == future_emb:
                        return ValidacionIdentidad(
                            success=True,
                            user_id=user_id,
                            pr_embedding=True,
                            pr_landmarks=False,
                        )
                    else:
                        return ValidacionIdentidad(
                            success=True,
                            user_id=user_id,
                            pr_embedding=False,
                            pr_landmarks=True,
                        )
            except Exception as e:
                print(f"Error en validación paralela: {e}")
                continue
    return None


def _comparar_muestras(
    muestras: List[Muestra],
    users_with_samples: List[Usuario],
) -> ValidacionIdentidad:
    if not muestras or not users_with_samples:
        return ValidacionIdentidad(success=False)

    # Evento para detener todos los hilos una vez que se encuentre una coincidencia
    encontrado_event = threading.Event()
    resultado = ValidacionIdentidad(success=False)

    def evaluar_muestra(muestra: Muestra) -> Optional[ValidacionIdentidad]:
        """
        Evalúa una muestra individual con ambos métodos en paralelo.
        Retorna un ValidacionIdentidad si hay coincidencia, o None si no.
        """
        if encontrado_event.is_set():
            return None  # Ya se encontró un resultado, no procesar más

        current_embedding = muestra.embedding
        current_landmarks = muestra.landmarks

        # Ejecutar embedding y landmarks en paralelo para esta muestra
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_emb = executor.submit(
                validar_embedding, current_embedding, users_with_samples
            )
            future_lmk = executor.submit(
                validar_landmarks, current_landmarks, users_with_samples
            )

            # Esperar el primero que termine y tenga éxito
            for future in concurrent.futures.as_completed([future_emb, future_lmk]):
                if encontrado_event.is_set():
                    return None  # Ya resuelto por otra muestra

                try:
                    user_id = future.result()
                    if user_id is not None:
                        # Determinar qué método tuvo éxito
                        if future == future_emb:
                            return ValidacionIdentidad(
                                success=True,
                                user_id=user_id,
                                pr_embedding=True,
                                pr_landmarks=False,
                            )
                        else:
                            return ValidacionIdentidad(
                                success=True,
                                user_id=user_id,
                                pr_embedding=False,
                                pr_landmarks=True,
                            )
                except Exception as e:
                    print(f"Error en validación paralela: {e}")
                    continue

        return None

    # Procesar todas las muestras en paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_muestra = {
            executor.submit(evaluar_muestra, muestra): muestra for muestra in muestras
        }

        for future in concurrent.futures.as_completed(future_to_muestra):
            if encontrado_event.is_set():
                break

            try:
                res = future.result()
                if res and res.success:
                    resultado = res
                    encontrado_event.set()  # Señalizar que ya se encontró
                    # Cancelar todas las tareas pendientes
                    for f in future_to_muestra:
                        f.cancel()
                    break
            except concurrent.futures.CancelledError:
                continue
            except Exception as e:
                print(f"Error procesando una muestra: {e}")

    return resultado


def run_identity_phase(
    db: Session,
    camera_index: int = 0,
    show_preview: bool = False,
    duration_capture: int = 5,
    from_terminal: bool = False,
) -> ValidacionIdentidad:

    if from_terminal:
        print(
            f"\n--- FASE 2: IDENTIFICACIÓN FACIAL (Capturando por {duration_capture}s) ---"
        )
        print("Mire fijamente a la cámara...")
        time.sleep(4)

    # capturar todos los frames
    resultado_muestras = get_muestras_with_b64(
        camera_index=camera_index,
        duration_capture=duration_capture,
        show_preview=show_preview,
    )
    if not resultado_muestras:
        print("No se pudo capturar frames para la identificación.")
        return ValidacionIdentidad(success=False)

    muestras, b64 = resultado_muestras

    users_with_samples = usuario_repository.get_all_with_samples(db)

    start_time = time.time()
    resultado = _comparar_muestras(muestras, users_with_samples)
    duration = round(time.time() - start_time, 2)

    print(
        f"Resultados: Embeddings: {resultado.pr_embedding} | Landmarks: {resultado.pr_landmarks}"
    )

    return ValidacionIdentidad(
        success=resultado.success,
        duration=duration,
        user_id=resultado.user_id,
        pr_embedding=resultado.pr_embedding,
        pr_landmarks=resultado.pr_landmarks,
        b64=b64,
    )
