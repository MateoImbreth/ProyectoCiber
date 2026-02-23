from fastapi import APIRouter, Depends, Form, Request, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from typing import Annotated
from jose import JWTError, jwt
from pathlib import Path

#Importaciones internas de nuestra estructura
from Backend.app.db.db import get_db
from Backend.app.Core.config import settings
from Backend.app.Core.security import create_token 
from Backend.app.services import auth_services
from Backend.app.Crud import users as crud_users
from Backend.app.schemas.user_schema import UserLogin, UserRead, UserUpdate

# Inicializar el Router
router = APIRouter()
templates_dir = Path(__file__).parent.parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# ----------------------------------------------------
# 1. Ruta: Página de inicio de sesión (login)
# ----------------------------------------------------
@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ----------------------------------------------------
# 2. Ruta: Manejar el inicio de sesión (login)
# ----------------------------------------------------
@router.post("/login", response_class=HTMLResponse)
def login(
    nick_name: Annotated[str, Form(...)],
    contrasena: Annotated[str, Form(...)],
    confirmar_contrasena: Annotated[str, Form(...)],
    db: Session = Depends(get_db)
):
    # Verificar contraseñas iguales del usuario
    if contrasena != confirmar_contrasena:
        return JSONResponse(status_code=400, content={"detail": "Las contraseñas no coinciden"})
    
    # Verificar credenciales del usuario
    user = auth_services.verificar_credenciales(nick_name, contrasena, db)
    print("Usuario autenticado:", user)
    if not user:
        return JSONResponse(status_code=401, content={"detail": "Credenciales inválidas"})

    usuario_db = crud_users.obtener_usuario_por_nickname(db, nick_name)
    # Crear el token JWT y establecerlo en una cookie segura
    token = create_token({"nick_name": usuario_db.nick_name})

    #Redirigir al usuario a la página del dashboard después del login enviando la cookie
    response = JSONResponse(content={"message": "Login exitoso", "redirect": "/dashboard"})
    response.set_cookie(key="access_token", value=token, max_age=settings.TOKEN_SECONDS_EXP, path="/", httponly=True) # 
    return response


# ----------------------------------------------------
# 3. Ruta: Dashboard protegido (requiere autenticación)
# ----------------------------------------------------
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    access_token: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db)
):
    if not access_token: # 
        return RedirectResponse(url="/", status_code=303)

    try:
        #Decodificar el token JWT para obtener la información del usuario
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        nick_name: str = payload.get("nick_name") # Obtener el nick_name del payload del token decodificado, si el token no es válido o ha expirado, esto lanzará una excepción JWTError que se captura en el bloque except
        # Para comprobar que el token es válido y no ha expirado, se decodifica el token utilizando la función jwt.decode de la biblioteca jose, pasando el token, la clave secreta y el algoritmo de encriptación. Si el token es válido, se obtiene el payload decodificado, que contiene la información del usuario (en este caso, el nick_name). Si el token no es válido o ha expirado, se lanzará una excepción JWTError que se captura en el bloque except, lo que hace que se redirija al usuario a la página de inicio de sesión.
        # El token co
        user = crud_users.obtener_usuario_por_nickname(db, nick_name)
        if not user: #
            return RedirectResponse(url="/", status_code=303)
        
        return templates.TemplateResponse(
            "dashboard.html",
            {"request": request, "nick_name": user.nick_name}
            )
    except JWTError:
        return RedirectResponse(url="/", status_code=303)
    

# ----------------------------------------------------
# 4. Ruta: Logout (cerrar sesión)
# ----------------------------------------------------
@router.get("/users/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    # Eliminar la cookie de la sesión del token JWT
    response.delete_cookie(key="access_token", path="/")
    return response

# ----------------------------------------------------
# 5. Ruta: Mostrar formulario de registro de usuario
# ----------------------------------------------------  
@router.get("/register", response_class=HTMLResponse)
def mostrar_formulario_registro(request: Request):
    """
    Lo que hace es mostrar la página html del formulario de registro de nuevo usuario.
    """
    return templates.TemplateResponse("register.html", {"request": request})

# La diferencia entre router.get y router.post es que el primero se utiliza para manejar solicitudes GET, que son típicamente usadas para obtener datos o mostrar páginas, 
# mientras que el segundo se utiliza para manejar solicitudes POST, que son usadas para enviar datos al servidor, como en el caso de un formulario de registro o inicio de sesión. 
# En este caso, router.get("/register") muestra el formulario de registro, mientras que router.post("/register") procesa los datos enviados por ese formulario para crear un nuevo usuario.
# Para mostrar el formulario de registro el frontend a través de un enlace o botón redirige al usuario a la ruta "/register" con una solicitud GET, 
# lo que hace que se muestre la página HTML del formulario. Luego, cuando el usuario completa el formulario y lo envía, se envía una solicitud POST a la misma ruta "/register" 
# con los datos del formulario, y el backend procesa esa solicitud para registrar al nuevo usuario utilizando la lógica definida en auth_services.registrar_nuevo_usuario.

@router.post("/register")
def crear_usuario_endpoint(
    nick_name: str = Form(...),
    contrasena: str = Form(...),
    grupo: int = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Endpoint para registrar un nuevo usuario.
    Recibe los datos del formulario y usar la lógica de auth_services.
    Solo llamamos al servicio y él se encarga de todo.
    """
    resultado =auth_services.registrar_nuevo_usuario(
        db, nick_name, contrasena, grupo, email
    )

    if isinstance(resultado, JSONResponse):
        return resultado

    # Redirigir al usuario al login después del registro
    return JSONResponse(
        status_code=201, 
        content={"message": "Usuario creado con éxito", "redirect": "/"}
    )


# ----------------------------------------------------
# 6. Ruta: Listar todos los usuarios
# ----------------------------------------------------
@router.get("/usuarios/", response_model=list[UserRead])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = crud_users.obtener_usuarios(db)
    return usuarios

# ----------------------------------------------------
# 7. Ruta: Listar usuario por id
# ----------------------------------------------------
@router.get("/usuarios/{id_usuario}", response_model=UserRead)
def obtener_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = crud_users.obtener_usuario_por_id(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# ----------------------------------------------------
# 8. Ruta: Actualizar usuario   
# ----------------------------------------------------
@router.put("/usuarios/{id_usuario}", response_model=UserRead)
def actualizar_usuario_endpoint(
    id_usuario: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    usuario_actualizado = crud_users.actualizar_usuario(db, id_usuario, user_update)
    if not usuario_actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_actualizado

# ----------------------------------------------------
# 9. Ruta: Eliminar usuario
# ----------------------------------------------------
@router.delete("/usuarios/{id_usuario}")
def eliminar_usuario_endpoint(id_usuario: int, db: Session = Depends(get_db)):
    exito = crud_users.borrar_usuario(db, id_usuario)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"detail": "Usuario eliminado exitosamente"}