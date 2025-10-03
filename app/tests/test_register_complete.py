from app.domain.dbconfig import get_session
from app.application.use_cases.register_user.register_complete import register_complete

# python -m app.tests.test_register_complete


def test_register_complete():
    print("Iniciando prueba de registro completo...")
    try:
        with get_session() as db:
            # Datos de usuario de prueba
            user_dni = "98765432"
            user_nombre = "Usuario Completo"
            user_email = "completo@email.com"

            # Llamamos al caso de uso principal
            result = register_complete(
                db,
                dni=user_dni,
                nombre=user_nombre,
                email=user_email,
                camera_index=0,
                duration_capture=4,
                show_preview=False,
            )

            if not result:
                print("\nFallo: No se pudo completar el registro completo.")
                return

            usuario_creado, operacion_creada = result

            if operacion_creada:
                print(
                    f"\nÉxito: Registro completo del usuario con Operación ID: {operacion_creada.id}"
                )
            else:
                print("\nFallo: No se pudo completar el registro de la operación.")
    except Exception as e:
        print(f"Fallo inesperado: {e}")
    finally:
        print("\nPrueba finalizada.")


test_register_complete()
