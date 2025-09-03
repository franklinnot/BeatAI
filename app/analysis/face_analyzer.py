import face_recognition
from typing import TypedDict


class DatosMuestra(TypedDict):
    embedding: list[float]
    landmarks: dict[str, list[tuple[int, int]]]


def analizar_rostro(frame) -> DatosMuestra | None:
    """
    Analiza un frame para extraer el embedding y los landmarks.
    Retorna un diccionario simple o None si no se detecta cara.
    """
    face_locations = face_recognition.face_locations(frame, model="hog")
    if not face_locations:
        return None

    face_location = face_locations[0]

    embeddings = face_recognition.face_encodings(frame, [face_location], model="large")
    landmarks_list = face_recognition.face_landmarks(frame, [face_location])

    if not embeddings or not landmarks_list:
        return None

    # Devolvemos un diccionario en lugar de un objeto de modelo
    return {"embedding": embeddings[0].tolist(), "landmarks": landmarks_list[0]}
