from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from app.Core.config import settings # Importamos la configuración centralizada de settings

engine = create_engine(settings.DATABASE_URL)


# 🚨 FUNCIÓN DE DEPENDENCIA DE LA DB 🚨
def get_db() -> Generator:
    """
    Proporciona una sesión de DB para las rutas. 
    Usa 'yield' para asegurar que la sesión se cierre después de la solicitud.
    """
    with Session(engine) as session:
        yield session

# --- Script de Creación de Tablas (Para ejecución directa) ---
def create_db_tables():
    print("\n--- Intentando crear tablas en PostgreSQL ---")

    # IMPORTANTE: Debemos importar los modelos aquí antes de llamar a create_all
    # para que SQLModel "sepa" que esas tablas existen.

    from app.models import user_model 
    SQLModel.metadata.create_all(bind=engine)
    print("¡ÉXITO! Tablas creadas.")

if __name__ == "__main__":
    create_db_tables()