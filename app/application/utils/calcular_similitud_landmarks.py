import numpy as np
from typing import Dict, Any


def calcular_similitud_landmarks(
    landmarks1: Dict[str, Any], landmarks2: Dict[str, Any]
) -> float:
    """
    Calcula una distancia simple entre dos conjuntos de landmarks.
    NOTA: Esta es una métrica simple y puede ser mejorada. Compara la
    distancia euclidiana promedio de todos los puntos de landmarks.
    """
    # Aplanar y normalizar los puntos de ambos conjuntos de landmarks
    points1 = np.array(
        [p for feature in landmarks1.values() for p in feature], dtype=float
    )
    points2 = np.array(
        [p for feature in landmarks2.values() for p in feature], dtype=float
    )

    # Normalizar para que sean invariantes a la escala y posición
    points1 -= np.mean(points1, axis=0)
    points2 -= np.mean(points2, axis=0)
    points1 /= np.linalg.norm(points1)
    points2 /= np.linalg.norm(points2)

    # Calcular el error cuadrático medio
    distance = np.mean(np.linalg.norm(points1 - points2, axis=1))
    return distance
