import sys
import os

from app.domain.dbconfig import get_session
from app.application.use_cases.register_user.register_complete import register_complete

# python -m app.scripts.test_registration

# Añade la importación del error específico
from sqlalchemy.exc import InvalidRequestError

print("Iniciando prueba de registro de usuario...")

db_generator = get_session()
db = next(db_generator)

try:
    # Datos del nuevo usuario
    user_dni = "12345678"
    user_nombre = "Usuario de Prueba"
    user_email = "prueba@email.com"

    # Llamamos al caso de uso
    usuario_creado = register_complete(
        db,
        dni=user_dni,
        nombre=user_nombre,
        email=user_email,
        camera_index=0,
        duration=2,
    )

    # ELIMINA db.commit() DE AQUÍ. LO HACE register_complete.

    if usuario_creado:
        print(
            f"\n✅ Éxito: Usuario '{usuario_creado.nombre}' registrado correctamente."
        )
    else:
        print("\n❌ Fallo: No se pudo completar el registro del usuario.")
except InvalidRequestError as e:
    print(f"❌ Fallo de SQLAlchemy: {e}")
    db.rollback()
except RuntimeError as e:
    print(f"❌ Error de tiempo de ejecución: {e}")
    db.rollback()
    print(
        "Esto podría ser un problema con la configuración de la GPU o con las librerías dlib/cuDNN. "
        "Por favor, revisa tus drivers o la compatibilidad de las versiones."
    )
except Exception as e:
    print(f"❌ Fallo inesperado: {e}")
    db.rollback()
finally:
    db.close()
    print("\nPrueba finalizada.")
