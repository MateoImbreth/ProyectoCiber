from sqlmodel import Session, select
from app.models.user_model import Usuarios, Detalle_Usuarios
from app.schemas.user_schema import UserRead, UserUpdate
from app.Core.security import hash_password

# ----------------------------------------------------
# 1. Obtener usuario por ID
# ----------------------------------------------------

def obtener_usuario_por_id(db: Session, id_usuario: int):
    return db.get(Usuarios, id_usuario) 

# ----------------------------------------------------
# 2. Obtener usuario por nick_name
# ----------------------------------------------------

def obtener_usuario_por_nickname(db: Session, nick_name: str):
    statement = select(Usuarios).where(Usuarios.nick_name == nick_name)
    return db.exec(statement).first()


# ----------------------------------------------------
# 3. Crear nuevo usuario y sus detalles
# ----------------------------------------------------

def crear_useario_compleot(db: Session, user_data: dict, detail_data: dict):
    """
    1. Crea el registro del usuario en la tabla Usuarios.
    2. Usa el ID generado para crear el registro en Detalle_Usuarios.
    """
    # Crear eñ objeto del Modelo Usuarios
    nuevo_usuario = Usuarios(
        nick_name=user_data['nick_name'],
        nombre=user_data.get('nombre'),
        fecha=user_data['fecha']
    )
    db.add(nuevo_usuario)
    db.commit() # Guardar para obtener el ID generado
    db.refresh(nuevo_usuario) # Refrescar para obtener el ID

    # Crear el objeto del Modelo Detalle_Usuarios
    nuevo_detalle = Detalle_Usuarios(
        id_usuario= nuevo_usuario.id_usuario,
        contrasena= detail_data['contrasena'], # Asumimos que ya está hasheada
        grupo= detail_data['grupo'],
        email= detail_data['email'],
        estado_cuenta= True
    )

    db.add(nuevo_detalle)
    db.commit() # Guardar el detalle del usuario
    db.refresh(nuevo_detalle)

    return nuevo_usuario

# ----------------------------------------------------
# 4. Borrar usuario
# ----------------------------------------------------
def borrar_usuario(db: Session, id_usuario: int):
    usuario = db.get(Usuarios, id_usuario)
    if usuario:
        db.delete(usuario)
        db.commit()
        return True
    return False