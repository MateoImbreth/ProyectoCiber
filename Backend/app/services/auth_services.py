from sqlmodel import Session
from fastapi import HTTPException
from datetime import date
from Backend.app.Crud import users as crud_users
from Backend.app.Core.security import hash_password, verify_password

#----------------------------------------------------
# Servicio para registrar un nuevo usuario  
#----------------------------------------------------

def registrar_nuevo_usuario(db: Session, nick_name: str, contrasena: str, grupo: int, email: str):
    """
    Servicio para registrar un nuevo usuario.
    1. Verifica si el nick_name ya existe.
    2. Hashea la contraseña antes de guardarla.
    3. Crea el usuario y su detalle asociado.
    """
    # Verificar si el nick_name ya existe
    usuario_existente = crud_users.obtener_usuario_por_nickname(db, nick_name)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El nick_name ya está en uso.")

    # Hashear la contraseña
    contrasena_hasheada = hash_password(contrasena)

    # Preparar los datos para el CRUD
    datos_usuario = {
        'nick_name': nick_name,
        'fecha': date.today(),
        'nombre': None #Opcional
    }

    datos_detalle = {
        'contrasena': contrasena_hasheada,
        'grupo': grupo,
        'email': email
    }

    # Crear el usuario completo con el bibliotecario (CRUD) para que guarde
    nuevo_usuario = crud_users.crear_usuario_completo(db, datos_usuario, datos_detalle)
    return nuevo_usuario

#----------------------------------------------------
# Servicio para autenticar usuario (login)

def verificar_credenciales(nick_name: str, password_plana: str, db: Session):
    usuario_db = crud_users.obtener_usuario_por_nickname(db, nick_name)
    if not usuario_db or not usuario_db.detalles:
        return False
    return verify_password(password_plana, usuario_db.detalles[0].contrasena)