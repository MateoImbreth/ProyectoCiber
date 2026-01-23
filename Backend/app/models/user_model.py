from sqlmodel import Field, Relationship
from typing import Optional, List
from datetime import date
from Backend.app.db.base_class import Base

class Usuarios(Base, table=True):
    id_usuario: Optional[int] = Field(default=None,primary_key=True)
    nick_name: str = Field(max_length=50)
    fecha: date
    nombre: Optional[str] = None

    detalles: List["Detalle_Usuarios"] = Relationship(back_populates="usuarios")

class Detalle_Usuarios(Base, table=True):
    id_detalle_usuarios: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuarios.id_usuario", ondelete="CASCADE")
    contrasena: str
    token: Optional[str] = Field(default=None) 
    grupo: int
    email: str = Field(max_length=100)
    estado_cuenta: bool = Field(default=True)

    usuarios: Optional[Usuarios] = Relationship(back_populates="detalles")