from sqlalchemy.orm import Session
from typing import Optional
from app.domain.repositories.usuario_repository import usuario_repository
from app.domain.models import Usuario


def register_user(
    db: Session,
    *,
    dni: str,
    nombre: str,
    email: str,
) -> Optional[Usuario]:
    """
    Orquesta el proceso completo de registro de un usuario

    Verifica si el usuario existe, crea el registro
    """
    if usuario_repository.get_by_dni(db, dni=dni) or usuario_repository.get_by_email(
        db, email=email
    ):
        print(f"Error: El DNI '{dni}' o email '{email}' ya existen.")
        return None

    new_user = Usuario(dni=dni, nombre=nombre, email=email)
    created_user = usuario_repository.create(db, obj_in=new_user)
    print(f"Usuario '{created_user.nombre}' creado con ID: {created_user.id}")

    return created_user
