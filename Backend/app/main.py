from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import endpoints_auth # Importa las rutas de autenticación

# ----------------------------------------------------
# 1. Instancia de la Aplicación FastAPI
# ----------------------------------------------------

app = FastAPI(
    title="Plantilla",
    description="API para la autenticación multifactor (FastAPI + TOTP)",
    version="1.0.0",
)

# ----------------------------------------------------
# 2. Configuración CORS (Cross-Origin Resource Sharing)
# ----------------------------------------------------
origins = [
    "http://localhost:3000",  # Dirección típica de React Dev Server
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# 3. Inclusión de Rutas
# ----------------------------------------------------
app.include_router(endpoints_auth.router, tags=["Authentication"])

# ----------------------------------------------------
# 4. Rutas de prueba 
# ----------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "MFA Backend is running successfully!"}

@app.get("/status")
def get_status():
    """Ruta para comprobar el estado de la API."""
    return {"status": "OK", "service": "MFA API", "version": app.version}