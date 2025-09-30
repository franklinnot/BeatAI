import random

from app.domain.dbconfig import SessionLocal
from app.application.use_cases.identificacion.validar_complete import validar_complete


def test_validation_complete():
    print("--- INICIANDO PRUEBA DE FLUJO DE VALIDACIÓN COMPLETO ---")

    deditos = random.randint(2, 5)

    with SessionLocal() as db:
        acceso_concedido = validar_complete(
            db=db,
            cantidad_dedos_reto=deditos,
            camera_index=0,
            show_preview=True,
            duration_cap_liveness=3,
            duration_cap_identity=3,
        )

        # mostrar el resultado final de forma clara
        print("\n-------------------------------------------")
        print("---      RESULTADO FINAL DE LA PRUEBA     ---")
        print("-------------------------------------------")

        if acceso_concedido:
            print("\n✅ ACCESO PERMITIDO")
        else:
            print("\n🔒 ACCESO DENEGADO")
        print("\n-------------------------------------------")


# python -m app.tests.test_validacion_complete
test_validation_complete()
