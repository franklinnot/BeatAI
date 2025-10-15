import serial
import json
import time
from app.infraestructure.esp32.exec_prueba_vida import exec_prueba_vida
from app.infraestructure.esp32.exec_identificacion import exec_identificacion
from app.domain.dbconfig import get_session
from app.domain.models import Bitacora
from app.domain.repositories.usuario_repository import usuario_repository
from app.application.use_cases.identificacion.notificar import enviar_correo
import serial.tools.list_ports

print([p.device for p in serial.tools.list_ports.comports()])
camera_index = 1


import base64
import uuid
import os

PICTURES_DIR = "pictures"
os.makedirs(PICTURES_DIR, exist_ok=True)


def save_base64_image(b64_string: str) -> str:
    if not b64_string:
        raise ValueError("No se recibió base64 para guardar la imagen.")

    if "," in b64_string:
        b64_string = b64_string.split(",")[1]

    try:
        image_data = base64.b64decode(b64_string)
    except Exception:
        raise ValueError("Error al decodificar base64")

    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join(PICTURES_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(image_data)

    return filepath


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
                        enviar_respuesta(resultado)
                        print(f"[PC] → Respuesta enviada: {resultado}")
                        

                    elif solicitud == "PRUEBA_IDENTIFICACION" and bitacora:
                        print(f"[PC] Solicitud: {solicitud}")
                        resultado = exec_identificacion(
                            db, bitacora, camera_index=camera_index
                        )
                        enviar_respuesta(resultado.success)
                        print(f"[PC] → Respuesta enviada: {resultado.success}")

                        if resultado.b64:
                            try:
                                filepath = save_base64_image(resultado.b64 or "")
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
