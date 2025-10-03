from sqlalchemy.orm import Session
from typing import Optional
from app.domain.repositories.usuario_repository import usuario_repository
from app.domain.models import Usuario


def register_user(
    db: Session,
    dni: str,
    nombre: str,
    email: str,
) -> Optional[Usuario]:
    
    if usuario_repository.get_by_dni(db, dni=dni):
        print(f"Error: Ya existe un usuario con el DNI {dni}.")
        return None
    if usuario_repository.get_by_email(db, email=email):
        print(f"Error: Ya existe un usuario con el email {email}.")
        return None

    created_user = usuario_repository.create(
        db, obj_in=Usuario(dni=dni, nombre=nombre, email=email)
    )
    print(f"Usuario '{created_user.nombre}' creado con ID: {created_user.id}")

    return created_user
