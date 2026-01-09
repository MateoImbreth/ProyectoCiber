from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
# Importar Base desde el archivo simple base_class.py que creamos
from .base_class import Base

# --- Configuración de Conexión ---
db_user = 'nombre_usuario'
db_password = 'contraseña'
db_host = 'localhost'
db_port = 'puerto'
db_name = 'nombre_base_de_datos'

db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# --------------------------------

# 🚨 FUNCIÓN DE DEPENDENCIA DE LA DB 🚨
def get_db() -> Generator:
    """
    Proporciona una sesión de DB para las rutas. 
    Usa 'yield' para asegurar que la sesión se cierre después de la solicitud.
    """
    db = SessionLocal()
    try:
        yield db # La sesión se pasa a la función de la ruta
    finally:
        db.close() # Se asegura que la sesión se cierre SIEMPRE

# --- Script de Creación de Tablas (Para ejecución directa) ---
def create_db_tables():
    print("\n--- Intentando crear tablas en PostgreSQL ---")
    # Es crucial importar el modelo aquí para que Base.metadata lo conozca
    from ..models import user_model 
    Base.metadata.create_all(bind=engine)
    print("¡ÉXITO! Tablas creadas.")

if __name__ == "__main__":
    create_db_tables()