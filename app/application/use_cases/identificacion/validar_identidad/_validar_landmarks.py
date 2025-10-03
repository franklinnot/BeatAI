from typing import List, Optional, Dict, Any
from app.domain.models import Usuario
import numpy as np


def _calcular_similitud_landmarks(
    landmarks1: Dict[str, Any], landmarks2: Dict[str, Any]
) -> float:
    # Extraer y aplanar los puntos en un array de Numpy (N, 2)
    points1 = np.array(
        [p for feature in landmarks1.values() for p in feature], dtype=np.float32
    )
    points2 = np.array(
        [p for feature in landmarks2.values() for p in feature], dtype=np.float32
    )

    # Si no hay puntos, la distancia es infinita (no hay coincidencia)
    if points1.shape[0] == 0 or points2.shape[0] == 0 or points1.shape != points2.shape:
        return float("inf")

    # 1. Centrar los puntos (invariancia a la traslación)
    points1 -= np.mean(points1, axis=0)
    points2 -= np.mean(points2, axis=0)

    # 2. Normalizar la escala de los puntos (invariancia al tamaño/distancia)
    # Se divide por la norma de Frobenius, que es como la "magnitud" total de la nube de puntos.
    norm1 = np.linalg.norm(points1)
    norm2 = np.linalg.norm(points2)
    if norm1 == 0 or norm2 == 0:
        return float("inf")  # Evitar división por cero

    points1 /= norm1
    points2 /= norm2

    # 3. Calcular el Error Cuadrático Medio (MSE)
    # Es más rápido que la distancia euclidiana promedio y muy efectivo.
    distance = np.mean(np.sum((points1 - points2) ** 2, axis=1))

    return float(distance)


def validar_landmarks(
    current_landmarks: Dict[str, Any],
    users_with_samples: List[Usuario],
    threshold: float = 0.04,  # Umbral de distancia, ajustar según pruebas
) -> Optional[int]:
    
    if not users_with_samples or users_with_samples:
        return None

    best_match_user_id: Optional[int] = None
    min_overall_distance = float("inf")

    # Bucle para encontrar al mejor candidato global
    for user in users_with_samples:
        if not hasattr(user, "operaciones") or not user.operaciones:
            continue

        min_user_distance = float("inf")

        # Encontrar la mejor coincidencia (distancia más baja) para este usuario específico
        for operacion in user.operaciones:
            for muestra in operacion.muestras:
                distance = _calcular_similitud_landmarks(
                    muestra.landmarks, current_landmarks
                )
                if distance < min_user_distance:
                    min_user_distance = distance

        # Si la mejor distancia de este usuario es la mejor que hemos visto hasta ahora
        if min_user_distance < min_overall_distance:
            min_overall_distance = min_user_distance
            best_match_user_id = user.id

    # Después de revisar a TODOS los usuarios, verificamos si el mejor candidato es válido
    if best_match_user_id is not None and min_overall_distance < threshold:
        # ¡Éxito! El rostro más parecido está dentro de nuestro umbral de confianza.
        print(
            f"Mejor coincidencia por landmarks: ID {best_match_user_id} con distancia {min_overall_distance:.4f}"
        )
        return best_match_user_id

    # Si el mejor candidato no fue lo suficientemente bueno, no identificamos a nadie.
    return None
