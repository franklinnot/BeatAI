import concurrent.futures
from typing import TypedDict, Optional, List
import numpy as np

from app.domain.models import Usuario
from app.application.utils.get_emb_land import get_emb_land
from app.application.use_cases.identificacion.validar_embedding import validar_embedding
from app.application.use_cases.identificacion.validar_landmarks import validar_landmarks


class IdentificationResult(TypedDict):
    embedding_user_id: Optional[int]
    landmarks_user_id: Optional[int]
    error: Optional[str]


def validar_identificacion(
    frame: np.ndarray, users_with_samples: List[Usuario]
) -> IdentificationResult:
    """
    Procesa un frame para la identificación facial, ejecutando la validación
    de embeddings y landmarks en paralelo.
    """
    facial_data = get_emb_land(frame)
    if not facial_data:
        return {
            "embedding_user_id": None,
            "landmarks_user_id": None,
            "error": "No se detectó un único rostro.",
        }

    current_embedding, current_landmarks = facial_data

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_embedding = executor.submit(
            validar_embedding, current_embedding, users_with_samples
        )
        future_landmarks = executor.submit(
            validar_landmarks, current_landmarks, users_with_samples
        )

        embedding_user_id = future_embedding.result()
        landmarks_user_id = future_landmarks.result()

    return {
        "embedding_user_id": embedding_user_id,
        "landmarks_user_id": landmarks_user_id,
        "error": None,
    }
