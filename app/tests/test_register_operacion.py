from app.domain.dbconfig import get_session
from app.application.use_cases.register_user.register_operacion import (
    register_operacion,
)


# python -m app.tests.test_register_operacion


def test_register_operacion():
    print("Iniciando prueba de registro de usuario...")
    # La sesión debe manejarse fuera o el try/except dentro del 'with'
    try:
        with get_session() as db:
            # id del usuario
            usuario_id = 1

            operacion_creada = register_operacion(
                db,
                usuario_id=usuario_id,
                camera_index=0,
                duration_capture=4,  # Reducido para pruebas rápidas
                show_preview=False,
            )

            if operacion_creada and operacion_creada.total_muestras > 0:
                print(
                    f"\nÉxito: Operación '{operacion_creada.id}' registrada correctamente con {operacion_creada.total_muestras} muestras."
                )
            else:
                print(
                    "\nFallo: No se pudo completar el registro de la operacion o no se capturaron muestras."
                )

    except Exception as e:
        print(f"Fallo inesperado: {e}")


test_register_operacion()
