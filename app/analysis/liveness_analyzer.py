from scipy.spatial import distance as dist
import numpy as np

EAR_THRESHOLD = 0.23


def calculate_ear(eye_landmarks):
    A = dist.euclidean(eye_landmarks[1], eye_landmarks[5])
    B = dist.euclidean(eye_landmarks[2], eye_landmarks[4])
    C = dist.euclidean(eye_landmarks[0], eye_landmarks[3])
    return (A + B) / (2.0 * C)


def is_blinking(face_landmarks) -> bool:
    try:
        left_eye = np.array(face_landmarks["left_eye"])
        right_eye = np.array(face_landmarks["right_eye"])

        left_ear = calculate_ear(left_eye)
        right_ear = calculate_ear(right_eye)

        avg_ear = (left_ear + right_ear) / 2.0
        return avg_ear < EAR_THRESHOLD
    except (KeyError, IndexError):
        return False
