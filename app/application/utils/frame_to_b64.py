import cv2
import base64


def frame_a_base64(frame) -> str | None:
    exito, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

    if not exito:
        print("No se pudo codificar el frame en formato JPEG.")
        return None

    frame_bytes = buffer.tobytes()
    base64_encoded = base64.b64encode(frame_bytes)
    return base64_encoded.decode("utf-8")