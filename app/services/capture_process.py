import cv2
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.analysis.face_analyzer import analizar_rostro, DatosMuestra


async def capturar_y_procesar(duration_seconds: int = 5) -> list[DatosMuestra]:
    """Captura frames de la cámara y los procesa en paralelo."""
    print(
        f"📸 Mirando a la cámara. El proceso durará unos {duration_seconds} segundos."
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se puede abrir la cámara.")
        return []

    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=16)

    tasks = []
    start_time = asyncio.get_event_loop().time()

    while (asyncio.get_event_loop().time() - start_time) < duration_seconds:
        ret, frame = cap.read()
        if not ret:
            break
        task = loop.run_in_executor(executor, analizar_rostro, frame)
        tasks.append(task)
        await asyncio.sleep(0.05)

    cap.release()
    results = await asyncio.gather(*tasks)

    valid_results: list[DatosMuestra] = [res for res in results if res is not None]
    return valid_results
