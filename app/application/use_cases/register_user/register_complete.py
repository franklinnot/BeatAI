import time
from sqlalchemy.orm import Session
from typing import Optional
from app.domain.repositories.usuario_repository import usuario_repository
from app.domain.repositories.operacion_repository import operacion_repository
from app.domain.models.usuario_model import Usuario
from app.domain.models.operacion_model import Operacion
from app.application.use_cases.register_user.register_operacion import (
    register_operacion,
)
from app.application.use_cases.register_user.register_user import register_user


def register_complete(
    db: Session,
    *,
    dni: str,
    nombre: str,
    email: str,
    camera_index: int = 0,
    duration: int = 4,
) -> Optional[Usuario]:
    """
    Orquesta el proceso completo de registro de un usuario y la captura de sus muestras faciales.

    Verifica si el usuario existe, crea el registro, coordina la captura de muestras
    y actualiza la operación en la base de datos.
    """

    new_user = register_user(db=db, dni=dni, nombre=nombre, email=email)

    if not new_user:
        print("Error al crear el usuario.")
        return None
    new_operation = register_operacion(
        db=db, usuario_id=new_user.id, camera_index=camera_index, duration=duration
    )

    if not new_operation:
        print("Error al crear la operación de registro.")
        return None
    return new_user
