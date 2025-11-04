import serial
import json
import time
from app.infraestructure.esp32.exec_prueba_vida import exec_prueba_vida
from app.infraestructure.esp32.exec_identificacion import exec_identificacion
from app.domain.dbconfig import get_session
from app.domain.models import Bitacora
from app.domain.repositories.usuario_repository import usuario_repository
from app.domain.repositories.bitacora_repository import bitacora_repository
from app.application.use_cases.identificacion.notificar import enviar_correo
import serial.tools.list_ports
from pathlib import Path

print([p.device for p in serial.tools.list_ports.comports()])
camera_index = 1


import base64
import uuid
import os

PICTURES_DIR = "pictures"
os.makedirs(PICTURES_DIR, exist_ok=True)


def save_base64_image(id_carpeta: int, b64_string: str, filename: str) -> str:
    if not b64_string:
        print("No se recibió base64 para guardar la imagen.")
        return ""

    # Limpia el prefijo si viene en formato data:image/png;base64,...
    if "," in b64_string:
        b64_string = b64_string.split(",")[1]

    # Decodifica el base64
    try:
        image_data = base64.b64decode(b64_string)
    except Exception:
        print("Error al decodificar base64")
        return ""

    # Crea la carpeta destino si no existe
    base_path = Path(PICTURES_DIR)
    folder_path = base_path / str(id_carpeta)
    folder_path.mkdir(parents=True, exist_ok=True)

    # Ruta del archivo
    filepath = folder_path / f"{filename}.jpg"

    # Guarda la imagen
    try:
        with open(filepath, "wb") as f:
            f.write(image_data)
    except Exception as e:
        print(f"No se pudo guardar la imagen: {e}")
        return ""

    # Devuelve el path absoluto de la carpeta contenedora
    return str(folder_path.resolve())


def listen():
    try:
        ser = serial.Serial("COM5", 115200, timeout=1)
        time.sleep(2)  # esperar que Arduino reinicie
        print("[PC] Escuchando...")

        def enviar_respuesta(valor_bool):
            msg = {"respuesta": "True" if valor_bool else "False"}
            ser.write((json.dumps(msg) + "\n").encode("utf-8"))

        bitacora = None
        while True:
            if ser.in_waiting > 0:
                with get_session() as db:
                    line = ser.readline().decode("utf-8").strip()
                    if not line:
                        continue

                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    solicitud = data.get("solicitud", "")
                    if solicitud == "PRUEBA_VIDA":
                        cantidad_dedos = int(data.get("cantidad_dedos"))
                        print(f"[PC] Solicitud: {solicitud} ({cantidad_dedos} dedos)")
                        new_bitacora, resultado = exec_prueba_vida(
                            db, cantidad_dedos, camera_index=camera_index
                        )
                        bitacora = new_bitacora
                        enviar_respuesta(resultado.success)
                        print(f"[PC] → Respuesta enviada: {resultado.success}")

                        if resultado.b64:
                            try:
                                filepath = save_base64_image(
                                    bitacora.id, resultado.b64 or "", "prueba_vida"
                                )
                                print(f"[PC] Imagen guardada en: {filepath}")

                                bitacora_db = bitacora_repository.get_by_id(db, bitacora.id)
                                if bitacora_db:
                                    bitacora_repository.update(
                                        db,
                                        bitacora_db,
                                        {
                                            "path": filepath,
                                        },
                                    )
                            except Exception as e:
                                print(f"[PC] Error al guardar imagen: {e}")

                    elif solicitud == "PRUEBA_IDENTIFICACION" and bitacora:
                        print(f"[PC] Solicitud: {solicitud}")
                        resultado = exec_identificacion(
                            db, bitacora, camera_index=camera_index
                        )
                        enviar_respuesta(resultado.success)
                        print(f"[PC] → Respuesta enviada: {resultado.success}")

                        if resultado.b64:
                            try:
                                filepath = save_base64_image(
                                    bitacora.id,
                                    resultado.b64 or "",
                                    "prueba_identificacion",
                                )
                                print(f"[PC] Imagen guardada en: {filepath}")
                            except Exception as e:
                                print(f"[PC] Error al guardar imagen: {e}")

                        if resultado.success and resultado.user_id:
                            usuario = usuario_repository.get_by_id(
                                db, resultado.user_id
                            )
                            if usuario:
                                enviar_correo(
                                    nombre=usuario.nombre,
                                    email=usuario.email,
                                    b64=resultado.b64 or "",
                                    hora=bitacora.created_at,
                                )
                        bitacora = None

                    else:
                        continue

    except serial.SerialException as e:
        print(f"[ERROR] No se pudo abrir el puerto serial: {e}")

    except KeyboardInterrupt:
        print("\n[PC] Finalizando programa...")

    finally:
        if "ser" in locals() and ser.is_open:
            ser.close()
            print("[PC] Puerto serial cerrado correctamente.")
