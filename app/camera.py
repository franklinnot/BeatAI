import cv2


def capture_frame():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("No se pudo acceder a la cámara")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise RuntimeError("No se pudo capturar un frame de la cámara")

    # frame es un numpy array en formato BGR
    return frame


def capture_frames(n=5):
    """Captura varios frames para procesos que necesitan más contexto, ej. prueba de vida"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("No se pudo acceder a la cámara")

    frames = []
    for _ in range(n):
        ret, frame = cap.read()
        if ret:
            frames.append(frame)

    cap.release()
    return frames
