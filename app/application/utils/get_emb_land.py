import numpy as np
from typing import Optional, List, Tuple, Dict
import cv2
import concurrent.futures
from app.application.utils.get_face_embeddings import get_face_embeddings
from app.application.utils.get_face_landmarks import get_face_landmarks
from app.application.utils.get_face_locations import get_face_locations


def get_emb_land(frame: np.ndarray) -> Optional[Tuple[List[float], Dict]]:
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

    if len(locations) != 1:
        return None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Enviar cada función a un hilo diferente.
        future_embedding = executor.submit(get_face_embeddings, rgb_frame, locations)
        future_landmarks = executor.submit(get_face_landmarks, rgb_frame, locations)

        # 3. Recolectar los resultados cuando estén listos.
        try:
            embeddings_result = future_embedding.result()
            if embeddings_result:
                # El resultado es una lista de embeddings, tomamos el primero.
                embedding = embeddings_result[0].tolist()

            landmarks_result = future_landmarks.result()
            if landmarks_result:
                # El resultado es una lista de diccionarios de landmarks, tomamos el primero.
                landmarks = landmarks_result[0]
        except Exception as e:
            print(f"Error durante el procesamiento facial en paralelo: {e}")
            return None

    # 4. Devolver el resultado combinado solo si ambas operaciones fueron exitosas.
    if embedding and landmarks:
        return embedding, landmarks

    return None
