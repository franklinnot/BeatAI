import cv2
import face_recognition
from data.face_geometry import FaceGeometry


def process_geometry(user_id, frame, db, validation=False):
    # Convertir a RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar caras
    face_locations = face_recognition.face_locations(rgb_frame)

    if not face_locations:
        return None

    # Tomar la primera cara encontrada
    top, right, bottom, left = face_locations[0]

    if validation:
        # Buscar en DB coincidencias por geometría (ejemplo simplificado)
        geometries = db.query(FaceGeometry).all()
        for geom in geometries:
            data = geom.geometry_data
            if abs(data["top"] - top) < 10 and abs(data["left"] - left) < 10:
                return geom.user_id
        return None
    else:
        # Guardar en DB en formato JSON
        geometry = FaceGeometry(
            user_id=user_id,
            geometry_data={
                "top": top,
                "right": right,
                "bottom": bottom,
                "left": left,
            },
        )
        db.add(geometry)
        db.commit()
        db.refresh(geometry)
        return user_id
