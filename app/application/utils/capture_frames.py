import cv2
import time
from typing import List, Optional
import numpy as np


def capture_frames(
    camera_index: int,
    duration: int,
    show_preview: bool = False,
    cap_instance: Optional[cv2.VideoCapture] = None,
) -> List[np.ndarray]:
    """
    Captura frames de una cámara durante una duración específica.
    Puede reutilizar una instancia de VideoCapture si se proporciona.
    """
    # Si no se pasa una instancia de cámara, crea una nueva.
    # Si se pasa, la variable local 'cap' apunta a esa instancia existente.
    cap = cap_instance or cv2.VideoCapture(camera_index)

    # Nos aseguramos de que la cámara esté realmente abierta.
    if not cap.isOpened():
        print("Error: La instancia de la cámara no está abierta.")
        return []

    frames = []
    start_time = time.time()

    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            continue
        frames.append(frame)

        if show_preview:
            # Se usa un nombre de ventana específico para evitar conflictos.
            cv2.imshow("Capturando Frames", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    # IMPORTANTE: Solo se libera la cámara si fue creada DENTRO de esta función.
    # Si fue pasada como parámetro, la función que la creó se encargará de cerrarla.
    if not cap_instance:
        cap.release()

    if show_preview:
        # Se cierra solo la ventana que esta función pudo haber creado.
        cv2.destroyWindow("Capturando Frames")

    return frames
