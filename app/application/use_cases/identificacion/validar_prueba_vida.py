import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Tuple
import time
import concurrent.futures
from app.application.utils.capture_frames import capture_frames
from app.application.use_cases.identificacion.types.validacion_vida_class import (
    ValidacionVida,
)


mp_hands = mp.solutions.hands  # type: ignore


def _crear_detector_manos() -> mp.solutions.hands.Hands:  # type: ignore
    """Función auxiliar para encapsular la creación del detector."""
    return mp.solutions.hands.Hands(  # type: ignore
        static_image_mode=True,  # True para procesar imágenes individuales
        max_num_hands=2,
        min_detection_confidence=0.7,
    )


def _validar_frame_prueba_vida(frame: np.ndarray, cantidad_dedos_reto: int) -> bool:
    """
    Valida la cantidad de dedos levantados.
    """
    if frame is None:
        return False

    hands = _crear_detector_manos()
    try:
        # Procesamiento de la imagen
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Si no se detectan manos, la validación falla
        if not results.multi_hand_landmarks:
            return False

        # Itera sobre cada mano detectada en la imagen
        for hand_landmarks, handedness in zip(
            results.multi_hand_landmarks, results.multi_handedness
        ):
            dedos_levantados = 0
            etiqueta_mano = handedness.classification[0].label
            es_mano_derecha = etiqueta_mano == "Right"

            # Índices de las puntas de los dedos
            puntas_ids = [4, 8, 12, 16, 20]  # Pulgar, Índice, Medio, Anular, Meñique

            # --- Lógica para los 4 dedos (Índice a Meñique) ---
            # Un dedo está levantado si su punta está más arriba (y menor) que su articulación inferior (PIP).
            for i in range(1, 5):
                punta_dedo = hand_landmarks.landmark[puntas_ids[i]]
                articulacion_pip = hand_landmarks.landmark[puntas_ids[i] - 2]

                if punta_dedo.y < articulacion_pip.y:
                    dedos_levantados += 1

            # --- Lógica para el Pulgar (AJUSTADA PARA CÁMARA INVERTIDA / MODO ESPEJO) ---
            # Se compara la punta del pulgar con la articulación de justo debajo en el eje X.
            punta_pulgar = hand_landmarks.landmark[puntas_ids[0]]  # Landmark 4
            articulacion_ip = hand_landmarks.landmark[puntas_ids[0] - 1]  # Landmark 3

            if es_mano_derecha:
                # En modo espejo, la punta del pulgar derecho abierto está a la DERECHA de su base
                if punta_pulgar.x > articulacion_ip.x:
                    dedos_levantados += 1
            else:  # Mano Izquierda
                # En modo espejo, la punta del pulgar izquierdo abierto está a la IZQUIERDA de su base
                if punta_pulgar.x < articulacion_ip.x:
                    dedos_levantados += 1

            # --- Comparación Final ---
            # Si el conteo de esta mano coincide con el reto, la validación es exitosa.
            if dedos_levantados == cantidad_dedos_reto:
                return True

        # Si se revisaron todas las manos y ninguna coincidió, la validación falla.
        return False

    finally:
        # Asegura que los recursos del detector se liberen siempre
        hands.close()


def run_liveness_phase(
    cap: cv2.VideoCapture,
    camera_index: int,
    cantidad_dedos_reto: int,
    show_preview: bool,
    duration_cap_liveness: int = 5,
) -> ValidacionVida:
    """
    Ejecuta la fase de prueba de vida con la estrategia de 'capturar primero, procesar después'.
    """
    print(f"--- FASE 1: PRUEBA DE VIDA (Capturando por {duration_cap_liveness}s) ---")
    print(f"RETO: Muestre {cantidad_dedos_reto} dedo(s) a la cámara.")
    time.sleep(2)

    # capturar todos los frames
    frames = capture_frames(
        camera_index,
        duration=duration_cap_liveness,
        show_preview=show_preview,
        cap_instance=cap,
    )

    if not frames:
        print("❌ No se pudieron capturar frames para la prueba de vida.")
        return ValidacionVida(success=False, duration=None)

    start_time_liveness = time.time()
    # procesar todos los frames en paralelo.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(_validar_frame_prueba_vida, frame, cantidad_dedos_reto)
            for frame in frames
        }

        for future in concurrent.futures.as_completed(futures):
            # si CUALQUIER frame es válido, la prueba es un éxito.
            if future.result():
                duration = round(time.time() - start_time_liveness, 2)
                print(f"✅ Prueba de Vida SUPERADA en {duration}s.")
                # cancelar las tareas restantes para ahorrar recursos.
                for f in futures:
                    f.cancel()
                return ValidacionVida(success=True, duration=duration)

    print("❌ Falló la prueba de vida en todos los frames capturados.")
    return ValidacionVida(
        success=False, duration=round(time.time() - start_time_liveness, 2)
    )
