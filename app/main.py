import cv2
from data.database import db, create_tables
from data.usuario import Usuario
from data.bitacora import Bitacora
from onion.verify_geometry import process_geometry
from onion.verify_descriptors import process_descriptors
from onion.verify_liveness import process_liveness


def capture_frame():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se pudo acceder a la cámara")
        return None

    ret, frame = None, None
    for _ in range(5):
        ret, frame = cap.read()

    if not ret or frame is None:
        print("⚠️ No se pudo capturar la imagen desde la cámara")
        return

    cap.release()

    if not ret:
        print("Error al capturar frame")
        return None

    return frame


def capture_frames(count=3):
    cap = cv2.VideoCapture(0)
    frames = []
    if not cap.isOpened():
        print("No se pudo acceder a la cámara")
        return frames

    for _ in range(count):
        ret, frame = cap.read()
        if ret:
            frames.append(frame)

    cap.release()
    return frames


def registrar_usuario():
    nombre = input("Nombre: ")
    email = input("Email: ")

    user = Usuario(nombre=nombre, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)

    print("Captura tu rostro (1 imagen)...")
    frame = capture_frame()
    if frame is None:
        print("No se pudo capturar el rostro")
        return

    process_geometry(user.id, frame, db, validation=False)
    process_descriptors(user.id, frame, db, validation=False)

    db.commit()
    print(f"Usuario {nombre} registrado con ID {user.id}")


def validar_usuario():
    print("Validación en progreso...")

    frame = capture_frame()
    if frame is None:
        print("No se pudo capturar frame")
        return

    user_id_geom = process_geometry(None, frame, db, validation=True)
    user_id_desc = process_descriptors(None, frame, db, validation=True)

    bitacora = Bitacora(status=False, user_id=None)
    db.add(bitacora)

    if user_id_geom and user_id_desc and user_id_geom == user_id_desc: # type: ignore
        frames = capture_frames(3)
        liveness_ok = process_liveness(frames)

        if liveness_ok:
            bitacora.status = True # type: ignore
            bitacora.user_id = user_id_geom
            print(f"✅ Usuario validado con ID {user_id_geom}")
        else:
            print("❌ Prueba de vida fallida. No se asigna usuario.")
    else:
        print("❌ No hay coincidencia clara entre geometría y descriptores")

    db.commit()


def main():
    create_tables()

    while True:
        print("\nOpciones:")
        print("1. Registrar usuario")
        print("2. Validar usuario")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            validar_usuario()
        elif opcion == "3":
            break
        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()
