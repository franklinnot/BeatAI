import cv2
import face_recognition
from data.face_descriptors import FaceDescriptor


def process_descriptors(user_id, frame, db, validation=False):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_frame)

    if not encodings:
        return None

    encoding = encodings[0]

    if validation:
        stored_descs = db.query(FaceDescriptor).all()
        for desc in stored_descs:
            db_encoding = [float(x) for x in desc.descriptor_data]
            matches = face_recognition.compare_faces([db_encoding], encoding)
            if matches[0]:
                return desc.user_id
        return None
    else:
        descriptor = FaceDescriptor(
            user_id=user_id,
            descriptor_data=encoding.tolist(),  # ✅ guardamos como JSON (list)
        )
        db.add(descriptor)
        return user_id
