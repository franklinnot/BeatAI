from typing import List, Optional
from app.domain.models import Usuario
from app.application.utils.comparar_embeddings import comparar_embeddings
import numpy as np


def validar_embedding(
    current_embedding: List[float], users_with_samples: List[Usuario]
) -> Optional[int]:
    """
    Busca una coincidencia de usuario comparando embeddings.

    Args:
        current_embedding: Embedding del rostro en el frame actual.
        all_users_data: Lista de todos los usuarios con sus muestras precargadas.

    Returns:
        El ID del usuario si se encuentra una coincidencia, de lo contrario None.
    """
    for user in users_with_samples:
        known_embeddings = []
        for operacion in user.operaciones:
            for muestra in operacion.muestras:
                known_embeddings.append(muestra.embedding)

        if not known_embeddings:
            continue

        matches = comparar_embeddings(known_embeddings, current_embedding)

        # Si al menos una de las muestras coincide, consideramos al usuario identificado
        if np.any(matches):
            return user.id

    return None
