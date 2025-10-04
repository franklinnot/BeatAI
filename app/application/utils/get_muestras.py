import numpy as np
from typing import Optional, List, Tuple, Dict, Any
import cv2
import concurrent.futures
import face_recognition
from app.domain.models import Muestra
from app.application.utils.capture_frames import capture_frames
from app.application.utils.frame_to_b64 import frame_a_base64


# Type alias para mayor claridad
FaceLocation = List[tuple[int, int, int, int]]
FaceEmbedding = List[np.ndarray]
FaceLandmarks = List[Dict[str, Any]]


def _get_face_locations(frame: np.ndarray) -> FaceLocation:
    # el modelo 'hog' es más rápido y 'cnn' es más preciso pero lento
    return face_recognition.face_locations(frame, model="cnn")


def _get_face_landmarks(
    frame: np.ndarray, known_face_locations: FaceLocation
) -> FaceLandmarks:
    return face_recognition.face_landmarks(frame, known_face_locations, model="small")


def _get_face_embeddings(
    frame: np.ndarray, known_face_locations: FaceLocation
) -> FaceEmbedding:
    return face_recognition.face_encodings(frame, known_face_locations, model="small")


def _get_emb_land(frame: np.ndarray) -> Optional[Tuple[List[float], Dict]]:
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    locations = _get_face_locations(rgb_frame)

    if len(locations) != 1:
        return None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # enviar cada función a un hilo diferente.
        future_embedding = executor.submit(_get_face_embeddings, rgb_frame, locations)
        future_landmarks = executor.submit(_get_face_landmarks, rgb_frame, locations)

        # recolectar los resultados cuando estén listos.
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


def get_muestras(
    camera_index: int = 0,
    duration_capture: int = 4,
    show_preview: bool = False,
) -> List[Muestra] | None:

    frames = capture_frames(camera_index, duration_capture, show_preview)
    if not frames:
        print("No se pudo capturar frames de la cámara.")
        return None

    samples: List[Muestra] = []
    for frame in frames:
        result = _get_emb_land(frame)
        if result:
            embedding, landmarks = result
            new_sample = Muestra(landmarks=landmarks, embedding=embedding)
            samples.append(new_sample)
            if len(samples) >= 16:
                break
    return samples


def get_muestras_with_b64(
    camera_index: int = 0,
    duration_capture: int = 4,
    show_preview: bool = False,
) -> Tuple[List[Muestra], str] | None:

    frames = capture_frames(camera_index, duration_capture, show_preview)
    if not frames:
        print("No se pudo capturar frames de la cámara.")
        return None

    samples: List[Muestra] = []
    for frame in frames:
        result = _get_emb_land(frame)
        if result:
            embedding, landmarks = result
            new_sample = Muestra(landmarks=landmarks, embedding=embedding)
            samples.append(new_sample)
            if len(samples) >= 16:
                break

    mid = int(len(samples) / 2)
    b64 = frame_a_base64(frames[mid])
    return samples, b64 if b64 else ""
