import concurrent.futures
from typing import List
from app.application.utils.capture_frames import capture_frames
from app.application.utils.get_emb_land import get_emb_land
from app.domain.models import Muestra


def get_muestras(
    camera_index: int = 0,
    duration: int = 4,
    show_preview: bool = False,
) -> List[Muestra] | None:
    """
    Captura muestras faciales con una cámara y procesa los frames en paralelo.

    Args:
        db: Sesión de la base de datos.
        camera_index: Índice de la cámara a usar.
        duration: Duración de la captura en segundos.
        show_preview: Si es True, muestra una ventana de vista previa.

    Returns:
        Objetos de tipo muestra en una lista

    Raises:
        VideoCaptureFailed: Si no se puede abrir la cámara.
    """

    frames = capture_frames(camera_index, duration, show_preview)
    if not frames:
        print("No se pudo capturar frames de la cámara.")
        return None

    samples: List[Muestra] = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Enviar cada frame a un hilo para su procesamiento
        futures = {executor.submit(get_emb_land, frame): frame for frame in frames}

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result:
                    # Ggardar la muestra si el procesamiento fue exitoso
                    embedding, landmarks = result
                    new_sample = Muestra(
                        landmarks=landmarks,
                        embedding=embedding,
                    )
                    samples.append(new_sample)
                    print(samples)

                if len(samples) >= 16:
                    for pending_future in futures.keys():
                        pending_future.cancel()
                    break
            except concurrent.futures.CancelledError:
                # Ocurre cuando se llama a future.cancel(),
                # no es un error, es parte de la lógica.
                pass
            except Exception as e:
                print(f"Error procesando un frame: {e}")

    return samples
