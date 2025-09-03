from app.models._manager import db
from app.models.usuario import Usuario
from app.models.muestra import Muestra
from .capture_process import capturar_y_procesar

MIN_MUESTRAS_REGISTRO = 8


async def registrar_usuario(nombre: str, email: str, dni: str) -> Usuario | None:
    """Servicio completo para registrar un nuevo usuario y sus muestras biométricas."""
    if not nombre or not email or not dni:
        print("❌ Datos de usuario incompletos.")
        return None

    muestras_data = await capturar_y_procesar(duration_seconds=5)

    if len(muestras_data) < MIN_MUESTRAS_REGISTRO:
        print(
            f"❌ Muestras insuficientes ({len(muestras_data)}/{MIN_MUESTRAS_REGISTRO})."
        )
        return None

    # Primero, creamos el usuario en la base de datos
    nuevo_usuario = Usuario(nombre=nombre, email=email, dni=dni)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    # Luego, creamos y asociamos cada muestra
    for data in muestras_data:
        nueva_muestra = Muestra(
            user_id=nuevo_usuario.id,
            embedding=data["embedding"],
            landmarks=data["landmarks"],
        )
        db.add(nueva_muestra)

    db.commit()
    print(
        f"✅ Usuario '{nombre}' registrado con {len(muestras_data)} muestras biométricas."
    )
    return nuevo_usuario
