from typing import List, Optional, Dict, Any
from app.domain.models import Usuario
from app.application.utils.calcular_similitud_landmarks import (
    calcular_similitud_landmarks,
)


def validar_landmarks(
    current_landmarks: Dict[str, Any],
    users_with_samples: List[Usuario],
    threshold: float = 0.04,  # Umbral de distancia, ajustar según pruebas
) -> Optional[int]:
    """
    Busca una coincidencia de usuario comparando landmarks faciales
    Para cada usuario, encuentra la distancia mínima a sus muestras y verifica si
    supera el umbral.

    Args:
        current_landmarks: Landmarks del rostro en el frame actual.
        users_with_samples: Lista de todos los usuarios con sus muestras precargadas.
        threshold: Umbral de distancia para considerar una coincidencia.

    Returns:
        El ID del primer usuario que cumpla con el umbral de similitud.
    """
    for user in users_with_samples:
        if not user.operaciones:
            continue

        min_distancia_usuario = float("inf")

        # Encontrar la mejor coincidencia para ESTE usuario específico
        for operacion in user.operaciones:
            for muestra in operacion.muestras:
                distance = calcular_similitud_landmarks(
                    muestra.landmarks, current_landmarks
                )
                if distance < min_distancia_usuario:
                    min_distancia_usuario = distance

        # Solo si la mejor coincidencia de este usuario es suficientemente buena, lo identificamos
        if min_distancia_usuario < threshold:
            # Encontramos una coincidencia válida, no es necesario seguir buscando.
            return user.id

    # Si recorrimos todos los usuarios y ninguno cumplió el umbral, no hay coincidencia.
    return None
