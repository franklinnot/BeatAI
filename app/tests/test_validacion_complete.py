import random

from app.domain.dbconfig import SessionLocal
from app.application.use_cases.identificacion.validar_complete import validar_complete


def test_validation_complete():
    """
    Ejecuta el caso de uso completo de validación y muestra los resultados.
    """
    print("--- INICIANDO PRUEBA DE FLUJO DE VALIDACIÓN COMPLETO ---")
    print(
        "Asegúrate de tener al menos un usuario registrado con `test_register_complete.py`"
    )

    # 1. Definir el reto para la prueba de vida
    dedos_para_mostrar = random.randint(1, 5)

    # 2. Obtener una sesión de la base de datos
    with SessionLocal() as db:

        # 3. Llamar a la función principal de validación
        acceso_concedido = validar_complete(
            db=db,
            cantidad_dedos_reto=dedos_para_mostrar,
            camera_index=0,
            show_preview=True,
            timeout_identity=2,
            timeout_liveness=2,
        )

        # 4. Mostrar el resultado final de forma clara
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
