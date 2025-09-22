from typing import List, Dict, Any
import face_recognition
import numpy as np

# Type alias para mayor claridad
FaceLocation = List[tuple[int, int, int, int]]
FaceLandmarks = List[Dict[str, Any]]


def get_face_landmarks(
    frame: np.ndarray, known_face_locations: FaceLocation
) -> FaceLandmarks:
    """
    Obtiene los puntos característicos (landmarks) de cada rostro localizado.

    Args:
        frame: El frame que contiene los rostros.
        known_face_locations: La lista de ubicaciones obtenida de get_face_locations.

    Returns:
        Una lista de diccionarios, donde cada diccionario contiene los landmarks de un rostro.
        Estos diccionarios son directamente serializables a JSON.
    """
    return face_recognition.face_landmarks(frame, known_face_locations)
