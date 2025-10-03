from typing import List, Optional
from app.domain.models import Usuario
import numpy as np
import face_recognition


def _comparar_embeddings(
    known_embeddings: List[List[float]],
    current_embedding: List[float],
    tolerance: float = 0.6,
) -> np.ndarray:
    known_embeddings_np = [np.array(e) for e in known_embeddings]
    current_embedding_np = np.array(current_embedding)

    return face_recognition.compare_faces(
        known_embeddings_np, current_embedding_np, tolerance=tolerance
    )  # type: ignore


def validar_embedding(
    current_embedding: List[float], users_with_samples: List[Usuario]
) -> Optional[int]:
    for user in users_with_samples:
        known_embeddings = []
        for operacion in user.operaciones:
            for muestra in operacion.muestras:
                known_embeddings.append(muestra.embedding)

        if not known_embeddings:
            continue

        matches = _comparar_embeddings(known_embeddings, current_embedding)

        if np.any(matches):
            return user.id

    return None
