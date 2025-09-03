import sys
import os
import asyncio

# Agregar el directorio raíz del proyecto al path
# Esto asegura que los imports como 'from app...' funcionen correctamente
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models._manager import create_tables
from app.services.register_user import registrar_usuario
from app.services.validation_service import validar_usuario


def main():
    """Función principal que ejecuta el menú interactivo."""
    # Crea las tablas en la base de datos si no existen
    create_tables()

    while True:
        print("\n--- Sistema de Verificación Biométrica v2 ---")
        print("1. Registrar nuevo usuario")
        print("2. Validar identidad")
        print("3. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            # --- SECCIÓN ACTUALIZADA ---
            # Pedimos los datos al usuario de forma interactiva
            print("\n--- Registro de Nuevo Usuario ---")
            nombre = input("Nombre completo: ").strip()
            email = input("Correo electrónico: ").strip()
            dni = input("DNI (8 dígitos): ").strip()

            # Verificación simple para asegurar que los campos no estén vacíos
            if nombre and email and dni:
                asyncio.run(registrar_usuario(nombre, email, dni))
            else:
                print(
                    "\n❌ Error: Todos los campos son requeridos. Inténtalo de nuevo."
                )
            # --- FIN DE SECCIÓN ACTUALIZADA ---

        elif opcion == "2":
            asyncio.run(validar_usuario())

        elif opcion == "3":
            print("Saliendo del sistema. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Por favor, elige 1, 2 o 3.")


if __name__ == "__main__":
    main()
