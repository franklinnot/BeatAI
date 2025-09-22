from typing import List, Dict, Any
import face_recognition
import numpy as np

# Type alias para mayor claridad
FaceLocation = List[tuple[int, int, int, int]]


def get_face_locations(frame: np.ndarray) -> FaceLocation:
    """
    Encuentra la ubicación de todos los rostros en un frame.

    Args:
        frame: Un frame de imagen como un array de numpy.

    Returns:
        Una lista de tuplas con las coordenadas (top, right, bottom, left) de cada rostro.
    """
    # El modelo 'hog' es más rápido y bueno para CPUs. 'cnn' es más preciso pero lento.
    return face_recognition.face_locations(frame, model="hog")
