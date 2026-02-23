from sqlmodel import Field, Relationship
from typing import Optional, List
from datetime import date
from Backend.app.db.base_class import Base

# Aquí se guarda la información publica del usuario, como su nombre, fecha de registro, etc. Datos no sensibles.
class Usuarios(Base, table=True):
    id_usuario: Optional[int] = Field(default=None,primary_key=True)
    nick_name: str = Field(max_length=50)
    fecha: date
    nombre: Optional[str] = None

    detalles: List["Detalle_Usuarios"] = Relationship(back_populates="usuarios")

# Aquí se guarda la información sensible del usuario, como su contraseña, email, grupo, etc. Datos que no deben ser expuestos públicamente.
class Detalle_Usuarios(Base, table=True):
    id_detalle_usuarios: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuarios.id_usuario", ondelete="CASCADE") #ondelete="CASCADE" sirve para eliminar automáticamente los detalles asociados cuando se elimina un usuario
    contrasena: str
    token: Optional[str] = Field(default=None) 
    grupo: int
    email: str = Field(max_length=100)
    estado_cuenta: bool = Field(default=True)

    usuarios: Optional[Usuarios] = Relationship(back_populates="detalles")