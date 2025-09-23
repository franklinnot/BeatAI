from typing import List, Dict, Any
import face_recognition
import numpy as np

# Type alias para mayor claridad
FaceLocation = List[tuple[int, int, int, int]]
FaceEmbedding = List[np.ndarray]


def get_face_embeddings(
    frame: np.ndarray, known_face_locations: FaceLocation
) -> FaceEmbedding:
    """
    Calcula los embeddings faciales (vectores de 128 dimensiones) para los rostros localizados.

    Args:
        frame: El frame que contiene los rostros.
        known_face_locations: La lista de ubicaciones obtenida de get_face_locations.

    Returns:
        Una lista de embeddings, donde cada embedding es un array de numpy.
    """
    return face_recognition.face_encodings(frame, known_face_locations, model="small")
