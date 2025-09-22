from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


# base de datos en la raíz del proyecto ./app/database.db
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# engine y session
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # sqlite specific
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


def crear_tablas() -> None:
    try:
        import app.domain.models
    except Exception as e:
        print("Aviso: fallo al importar modelos:", e)
    Base.metadata.create_all(bind=engine)


def get_session() -> Generator:
    """
    Generador simple para obtener una sesión. Se usa como:

    with SessionLocal() as session:
        ...

    o

    db = next(get_session())
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
