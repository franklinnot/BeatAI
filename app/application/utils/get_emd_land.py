import numpy as np
from typing import Optional, List, Tuple, Dict
import cv2
from app.application.utils.get_face_embeddings import get_face_embeddings
from app.application.utils.get_face_landmarks import get_face_landmarks
from app.application.utils.get_face_locations import get_face_locations


def get_emd_land(frame: np.ndarray) -> Optional[Tuple[List[float], Dict]]:
    """
    Procesa un solo frame para encontrar rostros y extraer embeddings y landmarks.
    Si se encuentra exactamente un rostro, devuelve sus datos.

    Args:
        frame: Un frame de video en formato BGR.

    Returns:
        Una tupla con el embedding (como lista) y los landmarks, o None.
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    locations = get_face_locations(rgb_frame)

    if len(locations) == 1:
        embeddings = get_face_embeddings(rgb_frame, locations)
        landmarks = get_face_landmarks(rgb_frame, locations)

        if embeddings and landmarks:
            embedding = embeddings[0].tolist()
            return embedding, landmarks[0]

    return None
