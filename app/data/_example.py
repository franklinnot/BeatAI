# main.py
from database import create_tables

# Importa todos los modelos.
# Esto asegura que el mapeador de SQLAlchemy los "conozca" antes de crear las tablas.
from usuario import Usuario
from bitacora import Bitacora
from face_detector import FaceDetector
from face_features import FaceFeatures
from liveness import Liveness

# 1. Crea las tablas
create_tables()

# 2. Crea un nuevo usuario
usuario = Usuario(nombre="Break", email="break@email.com")
usuario.save()
print(f"Usuario guardado: {usuario}")

# 3. Busca el usuario por email
found_user = Usuario.find(email="break@email.com")
print(f"Usuario encontrado: {found_user}")

# 4. Actualiza el nombre del usuario
found_user.nombre = "Break_Final"
found_user.save()
print(f"Usuario actualizado: {found_user}")

# 5. Elimina el usuario
found_user.delete()
print(f"Usuario {found_user.id} eliminado")
