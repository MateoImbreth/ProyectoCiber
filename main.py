import bcrypt
import os

from sqlmodel import Field, Session, create_engine, select, SQLModel, Relationship
from typing import Annotated, Optional, List
from datetime import datetime, timedelta, date
from dotenv import load_dotenv

from fastapi import FastAPI,Request,Form, HTTPException, Cookie, Depends, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from fastapi.staticfiles import StaticFiles

from jose import jwt, JWTError

load_dotenv() #Carga lo del archivo .env

SECRET_KEY = os.environ.get("SECRET_KEY")
TOKEN_SECONDS_EXP = 20

#Conexión a la base de datos
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    with Session(engine) as session:
        yield session

# Función para hashear la contraseña
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()  # Genera un salt aleatorio
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) #Con encode se convierte el string de la contraseña en bytees
    return hashed_password.decode('utf-8') #Convierte la contraseña que fue converitda en bytes a String nuevamente


# Función para verificar la contraseña
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

#Define models
class Detalle_Usuarios(SQLModel, table=True):
    id_detalle_usuarios: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuarios.id_usuario", ondelete="CASCADE")
    contrasena: str
    token: Optional[str] = Field(default=None) 
    grupo: int
    email: str = Field(max_length=255)
    estado_cuenta: bool
    
    usuarios: "Usuarios" = Relationship(back_populates="detalles")

class Usuarios(SQLModel, table=True):
    id_usuario: Optional[int] = Field(default=None,primary_key=True)
    nick_name: str = Field(max_length=50)
    fecha: date
    nombre: Optional[str] = None

    detalles: list[Detalle_Usuarios] = Relationship(back_populates="usuarios")

class UsuarioActualizar(SQLModel):
    nick_name: Optional[str] = None
    fecha: Optional[date] = None
    nombre: Optional[str] = None
    contrasena: Optional[str] = None
    grupo: Optional[int] = None
    email: Optional[str] = None

jinja2_template = Jinja2Templates(directory="templates")

def get_user(username: str, db: Session = Depends(get_db)):
    statement = select(Usuarios).where(Usuarios.nick_name == username)
    try:
        user = db.exec(statement).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el usuario: {e}")
    return user

#
def authenticate_user(password_plane: str, user: Usuarios):
    if user and user.detalles and user.detalles:
        return verify_password(password_plane, user.detalles[0].contrasena)
    return False

def create_token(data: dict):
    data_token = data.copy()
    data_token["exp"] = datetime.utcnow() + timedelta(seconds=TOKEN_SECONDS_EXP)
    token_jwt = jwt.encode(data_token,key=SECRET_KEY,algorithm="HS256")
    return token_jwt 

@app.get("/",response_class=HTMLResponse) #Ruta base del logeo
def root(request: Request):
    return jinja2_template.TemplateResponse("index.html",{"request":request})

@app.get("/users/dashboard", response_class=HTMLResponse) #Ruta
def dashboard(request: Request, access_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    if access_token is None:
        return RedirectResponse("/", status_code=302)
    try:
        data_user = jwt.decode(access_token,key=SECRET_KEY,algorithms=["HS256"])
        user = get_user(data_user["username"], db)
        if user is None:
            return RedirectResponse("/", status_code=302)
        response = jinja2_template.TemplateResponse("dashboard.html",{"request": request, "username": user.nick_name})
        return response
    except JWTError:
        return RedirectResponse("/", status_code=302)
    except Exception as e:
        print(f"Error in dashboard: {e}")
        return RedirectResponse("/", status_code=302)

@app.post("/users/login") #Ruta a la que accedemos despues de logearnos
def login(username: Annotated[str,Form()], password: Annotated[str,Form()], confirmar_password: Annotated[str,Form()], db: Session = Depends(get_db)):
    user = get_user(username, db)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Nombre de usuario o contraseña incorrectos"
        )
    if not authenticate_user(password, user):
        raise HTTPException(
            status_code=401,
            detail="Nombre de usuario o contraseña incorrectos"
        )
    if password != confirmar_password:
        raise HTTPException(
            status_code=400,
            detail="Las contraseñas no coinciden"
        )
    token = create_token({"username": user.nick_name})

    user.detalles[0].token = token #Se actualiza el token en la db
    db.commit() #Se guarda el cambio en la db

    return RedirectResponse(
        "/users/dashboard",
        status_code=302,
        headers={"set-cookie": f"access_token={token}; Max-Age={TOKEN_SECONDS_EXP}; path=/"}
    )

@app.post("/users/logout")
def logout():
    return RedirectResponse("/",status_code=302,headers={
        "set-cookie": "access_token=; Max-Age=0; path=/"
    })

#CRUD
#Create
@app.post("/detalles_usuario/", response_model=Detalle_Usuarios, status_code=201)
def crear_detalles_usuario(
    nick_name: Annotated[str, Form()],
    contrasena: Annotated[str, Form()],
    grupo: Annotated[int, Form()],
    email: Annotated[str, Form()],
    db: Session = Depends(get_db),
    ):
    """
    Crea un nuevo usuario y sus detalles en la base de datos.
    """
    # Verificar si el nombre de usuario ya existe
    if db.execute(select(Usuarios).where(Usuarios.nick_name == nick_name)).first():
        raise HTTPException(status_code=400, detail="Nombre de usuario ya registrado")

    # Hashea la contraseña antes de guardarla
    hashed_contrasena = hash_password(contrasena)

    # Crear el usuario
    nuevo_usuario = Usuarios(nick_name=nick_name, fecha=date.today())  # Asigna la fecha de hoy
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)  # Obtener el ID del nuevo usuario

    # Crear los detalles del usuario
    token = create_token({"username": nick_name})  # Crea el token
    nuevo_detalle = Detalle_Usuarios(
        id_usuario=nuevo_usuario.id_usuario,
        contrasena=hashed_contrasena,  # Usar la contraseña hasheada
        grupo=grupo,
        email=email,
        estado_cuenta=True,  # Establecer el estado de la cuenta como verdadero
    )
    db.add(nuevo_detalle)
    db.commit()
    db.refresh(nuevo_detalle)

    return RedirectResponse("/", status_code=302)

#Read
@app.get("/usuarios/{usuario_id}", response_model=Usuarios)
def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un usuario por su ID.
    """
    usuario = db.get(Usuarios, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/usuarios/", response_model=List[Usuarios])
def leer_usuarios(db: Session = Depends(get_db), offset:int=0, limit: Annotated[int, Query(le=100)] = 100,):
    """
    Obtiene todos los usuarios.
    """
    usuarios = db.exec(select(Usuarios).offset(offset).limit(limit)).all()
    return usuarios

#UPDATE
@app.put("/usuarios/{usuario_id}", response_model=Usuarios)
def actualizar_usuario(
    usuario_id: int,
    usuario_actualizado: UsuarioActualizar,
    db: Session = Depends(get_db)
):
    usuario = db.get(Usuarios, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualiza los atributos del usuario si se proporcionan
    if usuario_actualizado.nick_name is not None:
        usuario.nick_name = usuario_actualizado.nick_name
    if usuario_actualizado.nombre is not None:
        usuario.nombre = usuario_actualizado.nombre
    if usuario_actualizado.fecha is not None:
        usuario.fecha = usuario_actualizado.fecha

    # Obtiene los detalles del usuario
    detalle_usuario = db.exec(
        select(Detalle_Usuarios).where(Detalle_Usuarios.id_usuario == usuario_id)
    ).first()

    if detalle_usuario:
        # Actualiza los detalles si se proporcionan
        if usuario_actualizado.contrasena is not None:
            hashed_contraseña = hash_password(usuario_actualizado.contrasena) #Hashear la nueva contraseña
            detalle_usuario.contrasena = usuario_actualizado.contrasena
        if usuario_actualizado.grupo is not None:
            detalle_usuario.grupo = usuario_actualizado.grupo
        if usuario_actualizado.email is not None:
            detalle_usuario.email = usuario_actualizado.email

        db.add(detalle_usuario)

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

#DELETE
@app.delete("/usuarios/{usuario_id}", response_model=dict)
def borrar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Elimina un usuario por su ID. Elimina explícitamente los detalles primero.
    """
    usuario = db.get(Usuarios, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Eliminar los detalles del usuario explícitamente
    detalles_usuario = db.exec(select(Detalle_Usuarios).where(Detalle_Usuarios.id_usuario == usuario_id)).all()
    for detalle in detalles_usuario:
        db.delete(detalle)
    db.commit()

    # Luego eliminar el usuario
    db.delete(usuario)
    db.commit()
    return {"message": f"Usuario {usuario.nick_name} y sus detalles eliminados correctamente"}

@app.get("/register", response_class=HTMLResponse)
def show_register_form(request: Request):
    """
    Muestra el formulario de registro.
    """
    return jinja2_template.TemplateResponse("register.html", {"request": request})

