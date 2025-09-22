import time
import cv2
import concurrent.futures
import threading
from typing import Optional, List, Any, Dict

# Importaciones de utilidades y modelos
from app.application.utils.capture_frames import capture_frames
from app.application.utils.get_emd_land import get_emd_land
from app.domain.models.muestra_model import Muestra
from app.domain.repositories.muestra_repository import muestra_repository
from app.domain.repositories.operacion_repository import operacion_repository
from sqlalchemy.orm import Session

def register_muestras(
    db: Session,
    operacion_id: int,
    camera_index: int = 0,
    duration: int = 4,
    show_preview: bool = False,
) -> int | None:
    """
    Captura muestras faciales de una cámara, procesa los frames en paralelo
    y los guarda en la base de datos.

    Args:
        db: Sesión de la base de datos.
        operacion_id: ID de la operación a la que se asociarán las muestras.
        camera_index: Índice de la cámara a usar.
        duration: Duración de la captura en segundos.
        show_preview: Si es True, muestra una ventana de vista previa.

    Returns:
        El número de muestras capturadas.

    Raises:
        VideoCaptureFailed: Si no se puede abrir la cámara.
    """

    frames = capture_frames(camera_index, duration, show_preview)
    if not frames:
        print("No se pudo capturar frames de la cámara.")
        return None

    muestras_count = 0
    samples: List[Muestra] = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Enviar cada frame a un hilo para su procesamiento
        futures = {executor.submit(get_emd_land, frame): frame for frame in frames}

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result:
                    # Ggardar la muestra si el procesamiento fue exitoso
                    embedding, landmarks = result
                    new_sample = Muestra(
                        operacion_id=operacion_id,
                        landmarks=landmarks,
                        embedding=embedding,
                    )
                    samples.append(new_sample)
                    muestras_count += 1
            except Exception as e:
                print(f"Error procesando un frame: {e}")
        
        # Guardar las muestras en la base de datos una por una
        for sample in samples:
            muestra_repository.create(db, obj_in=sample)

    return muestras_count
