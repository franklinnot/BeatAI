from sqlalchemy.orm import Session
from typing import Optional

#
from app.domain.models import Usuario, Operacion
from app.application.use_cases.register_user.register_operacion import (
    register_operacion,
)
from app.application.use_cases.register_user.register_user import register_user
from app.domain.classes import OperacionResultado


def register_complete(
    db: Session,
    dni: str,
    nombre: str,
    email: str,
    camera_index: int = 0,
    duration_capture: int = 4,
    show_preview: bool = False,
) -> Optional[tuple[Usuario, OperacionResultado]]:

    new_user = register_user(db=db, dni=dni, nombre=nombre, email=email)

    if not new_user:
        print("Error al crear el usuario.")
        return None

    new_operation = register_operacion(
        db=db,
        usuario_id=new_user.id,
        camera_index=camera_index,
        duration_capture=duration_capture,
        show_preview=show_preview,
    )

    if not new_operation:
        print("Error al crear la operación de registro.")
        return None

    return new_user, new_operation
