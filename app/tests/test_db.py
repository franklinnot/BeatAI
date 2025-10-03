from app.domain.dbconfig import get_session
from app.domain.models import Usuario
from app.domain.repositories.usuario_repository import usuario_repository

# Comando de ejecucion:
# python -m app.tests.test_db


def test_db():
    with get_session() as db:
        user = Usuario(dni="12345678", nombre="Juan Perez", email="juan@example.com")
        user = usuario_repository.create(db, obj_in=user)
        print("Usuario creado:", user.id, user.dni)

test_db()
