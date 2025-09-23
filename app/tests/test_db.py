from app.domain.dbconfig import crear_tablas, SessionLocal
from app.domain.models import Usuario

# Comando de ejecucion:
# python -m app.tests.test_db


def test_db():
    with SessionLocal() as db:
        user = Usuario(dni="12345678", nombre="Juan Perez", email="juan@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
        print("Usuario creado:", user.id, user.dni)

test_db()
