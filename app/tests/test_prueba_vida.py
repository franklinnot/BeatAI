import cv2
import mediapipe as mp
import numpy as np
from app.application.use_cases.identificacion.validar_prueba_vida import (
    validar_prueba_vida,
)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)


# python -m app.tests.test_prueba_vida

def test_validar_prueba_vida():
    cap = cv2.VideoCapture(0)

    # El reto es mostrar 3 dedos
    reto_dedos = 3
    print(f"Prueba de vida iniciada: Por favor, muestra {reto_dedos} dedos.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignorando frame vacío de la cámara.")
            continue

        frame = cv2.flip(frame, 1)  # Voltear horizontalmente para efecto espejo

        # Llamar a la función de validación
        es_valido = validar_prueba_vida(frame, reto_dedos)

        # Mostrar resultado en pantalla
        color = (0, 255, 0) if es_valido else (0, 0, 255)
        texto = (
            f"Muestra {reto_dedos} dedos: {'CORRECTO' if es_valido else 'INCORRECTO'}"
        )
        cv2.putText(
            frame, texto, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA
        )

        # Opcional: Dibujar los landmarks de la mano para depuración
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

        cv2.imshow("Prueba de Vida con MediaPipe", frame)

        if cv2.waitKey(5) & 0xFF == 27:  # Presiona ESC para salir
            break

    # Liberar recursos
    hands.close()
    cap.release()
    cv2.destroyAllWindows()
