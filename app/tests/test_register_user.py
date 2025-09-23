from app.domain.dbconfig import SessionLocal
from app.application.use_cases.register_user.register_user import register_user
from sqlalchemy.exc import InvalidRequestError


# Comando de ejecucion:
# python -m app.tests.test_register_user

def test_register_user():

    print("Iniciando prueba de registro de usuario...")

    try:
        with SessionLocal() as db:
            # Datos del nuevo usuario
            user_dni = "12345678"
            user_nombre = "Usuario de Prueba"
            user_email = "prueba@email.com"

            # Llamamos al caso de uso
            usuario_creado = register_user(
                db,
                dni=user_dni,
                nombre=user_nombre,
                email=user_email,
            )

            if usuario_creado:
                print(
                    f"\n✅ Éxito: Usuario '{usuario_creado.nombre}' registrado correctamente."
                )
            else:
                print("\n❌ Fallo: No se pudo completar el registro del usuario.")
    except Exception as e:
        print(f"❌ Fallo inesperado: {e}")
        db.rollback()
    finally:
        db.close()
        print("\nPrueba finalizada.")

test_register_user()
