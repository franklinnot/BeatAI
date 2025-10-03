import random
from app.application.use_cases.identificacion.validar_prueba_vida import run_liveness_phase


# python -m app.tests.test_prueba_vida

def test_validar_prueba_vida():
    cantidad_dedos_reto = random.randint(2, 5)
    isValid = run_liveness_phase(
        cantidad_dedos_reto=cantidad_dedos_reto,
        show_preview=True,
        camera_index=0,
        duration_capture=2,
        from_terminal=True,
    )

    if isValid:
        print("Prueba de vida superada")
    else:
        print("Prueba de vida fallida")


test_validar_prueba_vida()
