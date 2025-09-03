import numpy as np


def get_geometry_ratios(landmarks):
    """Calcula ratios faciales estables a partir de los landmarks."""
    try:
        # Distancia entre los ojos
        left_eye_center = np.mean(landmarks["left_eye"], axis=0)
        right_eye_center = np.mean(landmarks["right_eye"], axis=0)
        eye_distance = np.linalg.norm(left_eye_center - right_eye_center)

        # "Altura" de la nariz
        # --- CORRECCIÓN AQUÍ ---
        # Convertimos las tuplas a arrays de NumPy antes de la resta
        point1 = np.array(landmarks["nose_bridge"][0])
        point2 = np.array(landmarks["nose_tip"][2])
        nose_bridge_height = np.linalg.norm(point1 - point2)

        if eye_distance == 0 or nose_bridge_height == 0:
            return None

        # Ratio como una característica geométrica
        ratio1 = eye_distance / nose_bridge_height

        return {"eye_to_nose_ratio": ratio1}
    except (KeyError, IndexError):
        return None


def compare_geometry(probe_ratios, known_samples_landmarks, tolerance=0.2):
    """
    Compara los ratios de la cara de prueba con el promedio de los ratios conocidos.
    """
    if not probe_ratios:
        return False

    known_ratios = []
    for landmarks in known_samples_landmarks:
        ratios = get_geometry_ratios(landmarks)
        if ratios:
            known_ratios.append(ratios["eye_to_nose_ratio"])

    if not known_ratios:
        return False

    avg_known_ratio = np.mean(known_ratios)
    probe_ratio = probe_ratios["eye_to_nose_ratio"]

    # Comprueba si el ratio de prueba está dentro de una tolerancia del promedio conocido
    return abs(probe_ratio - avg_known_ratio) < tolerance
