from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///project.db", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Función para crear las tablas
def create_tables():
    Base.metadata.create_all(bind=engine)


# Función para obtener una sesión (o más bien, la única sesión)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Exponemos la sesión como una variable global para acceso directo
db = SessionLocal()
