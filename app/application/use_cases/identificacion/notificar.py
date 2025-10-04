import requests
import json
import time
import sys

URL = "http://127.0.0.1:8000/send-email"


def enviar_correo(nombre: str, email: str, b64: str, hora: str) -> None:
    payload = {}
    payload["nombre"] = nombre
    payload["email"] = email
    payload["hora"] = hora
    payload["b64"] = b64

    print(f"\nEnviando payload a {URL} ...")
    # print(json.dumps(payload, indent=2)[:100], "...")  # muestra solo inicio

    try:
        response = requests.post(URL, json=payload, timeout=15)
    except requests.exceptions.ConnectionError:
        print("API no disponible. Verifica que esté corriendo.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return

    print(f"\nCódigo de estado: {response.status_code}")
    try:
        print("Respuesta JSON:", response.json())
    except Exception:
        print("Respuesta cruda:", response.text)
