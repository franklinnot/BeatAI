import cv2


def process_liveness(frames, db=None):
    """
    frames: lista de varios frames capturados.
    Aquí puedes implementar un algoritmo real de prueba de vida.
    Por ahora, haremos un dummy: si hay más de un frame con diferencias -> True
    """
    if len(frames) < 2:
        return False

    diffs = 0
    for i in range(1, len(frames)):
        diff = cv2.absdiff(frames[i], frames[i - 1])
        if diff.sum() > 100000:  # umbral arbitrario
            diffs += 1

    return diffs >= 1
