import random
from app.domain.dbconfig import get_session
from app.application.use_cases.identificacion.validar_complete import validar_complete
import time

# python -m app.tests.test_validacion_complete

def test_validation_complete():
    print("--- INICIANDO PRUEBA DE FLUJO DE VALIDACIÓN COMPLETO ---")
    deditos = random.randint(2, 5)
    print(f"Muestre {deditos} dedo(s) a la cámara.")
    time.sleep(3)

    with get_session() as db:
        acceso_concedido = validar_complete(
            db=db,
            cantidad_dedos_reto=deditos,
            camera_index=0,
            show_preview=False,
            duration_cap_liveness=3,
            duration_cap_identity=3,
            from_terminal=True,
        )

        # mostrar el resultado final de forma clara

        if acceso_concedido:
            print("\nACCESO PERMITIDO")
        else:
            print("\nACCESO DENEGADO")
        print("\n-------------------------------------------")


# python -m app.tests.test_validacion_complete
test_validation_complete()
