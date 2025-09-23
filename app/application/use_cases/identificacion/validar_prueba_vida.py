import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands


def _crear_detector_manos() -> mp.solutions.hands.Hands:
    """Función auxiliar para encapsular la creación del detector."""
    return mp.solutions.hands.Hands(
        static_image_mode=True,  # Cambiado a True para procesar imágenes individuales
        max_num_hands=1,
        min_detection_confidence=0.7,
    )


def validar_prueba_vida(frame: np.ndarray, cantidad_dedos_reto: int) -> bool:
    """
    Valida la cantidad de dedos levantados. Esta función es ahora 'thread-safe',
    ya que crea su propia instancia del detector en cada llamada.
    """
    if frame is None:
        return False

    # Cada llamada a esta función crea su propio detector local.
    # Esto evita el conflicto cuando se llama desde múltiples hilos.
    hands = _crear_detector_manos()

    try:
        # 1. Optimización de Velocidad y Procesamiento
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        results = hands.process(frame_rgb)
        frame_rgb.flags.writeable = True

        # 2. Verificación de Detección
        if not results.multi_hand_landmarks:
            return False

        # 3. Lógica de Conteo de Dedos Robusta
        hand_landmarks = results.multi_hand_landmarks[0]
        dedos_levantados = 0

        puntos_referencia = [[4, 2], [8, 6], [12, 10], [16, 14], [20, 18]]

        # Lógica para los 4 dedos
        for i in range(1, 5):
            punta = hand_landmarks.landmark[puntos_referencia[i][0]]
            articulacion_inf = hand_landmarks.landmark[puntos_referencia[i][1]]
            if punta.y < articulacion_inf.y:
                dedos_levantados += 1

        # Lógica mejorada para el pulgar
        punta_pulgar = hand_landmarks.landmark[puntos_referencia[0][0]]
        articulacion_inf_indice = hand_landmarks.landmark[puntos_referencia[1][1]]
        if punta_pulgar.y < articulacion_inf_indice.y:
            dedos_levantados += 1

        # 4. Comparación Final
        return dedos_levantados == cantidad_dedos_reto

    finally:
        # Asegurarse de que los recursos del detector se liberen siempre.
        hands.close()
