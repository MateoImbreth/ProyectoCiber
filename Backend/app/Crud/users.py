from sqlmodel import Session, select
from Backend.app.models.user_model import Usuarios, Detalle_Usuarios
from Backend.app.schemas.user_schema import UserRead, UserUpdate
from Backend.app.Core.security import hash_password

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
# 2.1 Obtener todos los usuarios
# ----------------------------------------------------

def obtener_usuarios(db: Session, offset: int = 0, limit: int = 100):
    statement = select(Usuarios).offset(offset).limit(limit)
    return db.exec(statement).all()

# ----------------------------------------------------
# 2.2 Obtener usuario por email
# ----------------------------------------------------

def obtener_usuario_por_email(db: Session, email: str):
    statement = select(Detalle_Usuarios).where(Detalle_Usuarios.email == email)
    return db.exec(statement).first()

# ----------------------------------------------------
# 3. Crear nuevo usuario y sus detalles
# ----------------------------------------------------

def crear_usuario_completo(db: Session, user_data: dict, detail_data: dict):
    """
    1. Crea el registro del usuario en la tabla Usuarios.
    2. Usa el ID generado para crear el registro en Detalle_Usuarios.
    """
    # Crear el objeto del Modelo Usuarios
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
# 3.1 Actualizar usuario
# ----------------------------------------------------
def actualizar_usuario(db: Session, id_usuario: int, user_update: UserUpdate):
    usuario = db.get(Usuarios, id_usuario)
    if not usuario:
        return None

    data = user_update.model_dump(exclude_unset=True)
    for key in ["nick_name", "nombre", "fecha"]:
        if key in data:
            setattr(usuario, key, data[key])

    if usuario.detalles:
        detalle = usuario.detalles[0]  # Acceder al primer detalle
        for key in ["contrasena", "grupo", "email"]:
            if key in data:
                val = data[key]
                if key == "contrasena":
                    val = hash_password(val)
                    setattr(detalle, key, val)
                else:
                    setattr(detalle, key, val)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

# ----------------------------------------------------
# 4. Borrar usuario
# ----------------------------------------------------
def borrar_usuario(db: Session, id_usuario: int):
    usuario = db.get(Usuarios, id_usuario)
    if usuario:
        detalle_usuario = db.exec(
            select(Detalle_Usuarios).where(Detalle_Usuarios.id_usuario == id_usuario)
        ).first()

        db.delete(detalle_usuario)
        db.commit()
        db.delete(usuario)
        db.commit()
        return True
    return False