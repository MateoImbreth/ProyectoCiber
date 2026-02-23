from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel

#Importaciones internas
from Backend.app.api import endpoints_auth # Importa las rutas de autenticación
from Backend.app.db.db import engine # Importa el motor de la base de datos
from Backend.app.models import user_model

# ----------------------------------------------------
# 1. Instancia de la Aplicación FastAPI
# ----------------------------------------------------

app = FastAPI(
    title="Sistema de Autenticación",
    description="Backedn para un sistema de autenticación con MFA utilizando FastAPI y SQLModel.",
    version="1.0.0",
)

# ----------------------------------------------------
# 2. Configuración de BASE DE DATOS y MODELOS
# ----------------------------------------------------

@app.on_event("startup")
def on_startup():
    """Evento que se ejecuta al iniciar la aplicación.
    Crea las tablas de la base de datos si no existen.
    """
    SQLModel.metadata.create_all(engine)

# ----------------------------------------------------
# 3. Configuración CORS (Cross-Origin Resource Sharing)
# ----------------------------------------------------
origins = [
    "http://localhost:8000",  # Dirección típica de React Dev Server
    "http://127.0.0.1:8000",
    "https://proyectociber.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# 4. Archivos estáticos [CSS, JS, Imágenes]
# ----------------------------------------------------
#app.mount("/tailwindcss", StaticFiles(directory="tailwindcss"), name="tailwindcss") # Monta el directorio 'static' para servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static") # Monta el directorio 'static' para servir archivos estáticos
app.add_middleware(GZipMiddleware) # Habilita la compresión GZip para respuestas
# ----------------------------------------------------
# 5. Inclusión de Rutas
# ----------------------------------------------------
app.include_router(endpoints_auth.router, tags=["Authentication"])

# ----------------------------------------------------
# 6. Rutas de prueba 
# ----------------------------------------------------

@app.get("/status")
def get_status():
    """Ruta para comprobar el estado de la API."""
    return {"status": "OK", "service": "MFA API", "version": app.version}