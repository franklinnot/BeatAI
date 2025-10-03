import cv2
import time
from typing import List
import numpy as np


def capture_frames(
    camera_index: int,
    duration_capture: int,
    show_preview: bool = False,
) -> List[np.ndarray]:
    cv2.destroyAllWindows()

    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        cv2.destroyAllWindows()  # Asegurar limpieza
        return []

    frames = []
    start_time = time.time()
    frame_start = time.time()
    try:
        while time.time() - start_time < duration_capture:
            ret, frame = cap.read()
            if not ret:
                # Si no se lee en 2 segundos, asumir fallo
                if time.time() - frame_start > 2.0:
                    print("Cámara no responde.")
                    break
                time.sleep(0.01)
                continue
            frames.append(frame)
            frame_start = time.time()

            if show_preview:
                cv2.imshow("Capturando Frames", frame)
                # Permitir que OpenCV procese eventos (¡crucial!)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    finally:
        cap.release()
        if show_preview:
            cv2.destroyAllWindows()  # Liberar ventanas de OpenCV
        time.sleep(0.3)

    return frames
