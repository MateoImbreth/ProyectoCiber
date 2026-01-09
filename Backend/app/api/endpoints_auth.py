from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Any
from sqlalchemy.orm import Session # Necesario para la inyección de dependencia

# Importaciones de la aplicación (Asegúrate de que las rutas sean correctas: ..Core y ..db)

from ..db.db import get_db #  Importación de la dependencia de la DB
from ..Crud import users as crud_users # Importación del CRUD real

from datetime import timedelta

# Inicializar el Router
router = APIRouter()
