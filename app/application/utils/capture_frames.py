import cv2
import time
from typing import List, Tuple
import numpy as np


def capture_frames(
    camera_index: int, duration: int, show_preview: bool = False
) -> List[np.ndarray]:
    """
    Captura frames de una cámara durante una duración específica.

    Args:
        camera_index: El índice de la cámara.
        duration: Duración de la captura en segundos.
        show_preview: Si es True, muestra una ventana de vista previa.

    Returns:
        Una lista de frames capturados.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return []

    frames = []
    start_time = time.time()

    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            continue

        frames.append(frame)

        if show_preview:
            cv2.imshow("Registro", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    if show_preview:
        cv2.destroyAllWindows()

    return frames
