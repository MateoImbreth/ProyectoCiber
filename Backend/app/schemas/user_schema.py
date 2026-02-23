from sqlmodel import SQLModel
from typing import Optional, List
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

class DetalleRead(SQLModel):
    email: str
    grupo: int
    estado_cuenta: bool

# Con esta clase se muestra la información del usuario, pero sin incluir la contraseña ni el token, 
# ya que son datos sensibles que no deben ser expuestos públicamente. En su lugar, se incluyen los 
# detalles relevantes como el email, grupo y estado de la cuenta.
class UserRead(SQLModel):
    id_usuario: int
    nick_name: str
    fecha: date
    nombre: Optional[str] = None
    detalles: List[DetalleRead] = []