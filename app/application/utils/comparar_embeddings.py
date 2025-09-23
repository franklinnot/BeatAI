import face_recognition
import numpy as np
from typing import List


def comparar_embeddings(
    known_embeddings: List[List[float]],
    current_embedding: List[float],
    tolerance: float = 0.6,
) -> np.ndarray:
    """
    Compara un embedding actual con una lista de embeddings conocidos.

    Args:
        known_embeddings: Lista de embeddings de la base de datos.
        current_embedding: El embedding del rostro detectado en el frame.
        tolerance: Umbral de distancia. Menor valor es más estricto.

    Returns:
        Un array de booleanos indicando las coincidencias.
    """
    # face_recognition necesita arrays de numpy para comparar
    known_embeddings_np = [np.array(e) for e in known_embeddings]
    current_embedding_np = np.array(current_embedding)

    return face_recognition.compare_faces(
        known_embeddings_np, current_embedding_np, tolerance=tolerance
    )  # type: ignore
