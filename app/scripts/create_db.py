from app.domain.dbconfig import crear_tablas

# Comando de ejecucion:
# python -m app.scripts.create_db

if __name__ == "__main__":
    crear_tablas()
    print("Tablas creadas.")
