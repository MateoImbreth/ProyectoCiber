from sqlmodel import SQLModel
from typing import Optional
from datetime import date

#----------------------------------------------------
# 1. Para el log in
#----------------------------------------------------
class UserLogin(SQLModel):
    username: str
    password: str
    confirm_password: str

#----------------------------------------------------
# 2. Para actualizar un usuario
#----------------------------------------------------
class UserUpdate(SQLModel):
    nick_name: Optional[str] = None
    fecha: Optional[date] = None
    nombre: Optional[str] = None
    contrasena: Optional[str] = None
    grupo: Optional[int] = None
    email: Optional[str] = None

#----------------------------------------------------
# 3. Para mostrar la información del usuario (sin contraseña)
#----------------------------------------------------

class UserRead(SQLModel):
    id_usuario: int
    nick_name: str
    fecha: date
    nombre: Optional[str] = None
    email: str
    grupo: int
    estado_cuenta: bool