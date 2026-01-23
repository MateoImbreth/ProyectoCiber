from fastapi import APIRouter, Depends, Form, Request, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from typing import Annotated
from jose import JWTError, jwt

#Importaciones internas de nuestra estructura
from Backend.app.db.db import get_db
from Backend.app.Core.config import settings
from Backend.app.Core.security import create_token 
from Backend.app.services import auth_services
from Backend.app.Crud import users as crud_users

# Inicializar el Router
router = APIRouter()
templates = Jinja2Templates(directory="Backend/templates")

#----------------------------------------------------
# 1. Ruta: Página de inicio de sesión (login)
# ----------------------------------------------------
@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#----------------------------------------------------
# 2. Ruta: Manejar el inicio de sesión (login)
# ----------------------------------------------------
@router.post("/users/login", response_class=HTMLResponse)
def login(
    nick_name: Annotated[str, Form(...)],
    contrasena: Annotated[str, Form(...)],
    confirmar_contrasena: Annotated[str, Form(...)],
    db: Session = Depends(get_db)
):
    # Verificar contraseñas iguales del usuario
    if contrasena != confirmar_contrasena:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden.")
    
    # Verificar credenciales del usuario
    user = auth_services.verificar_credenciales(db, nick_name, contrasena)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Crear el token JWT y establecerlo en una cookie segura
    token = create_token({"nick_name": user.nick_name})

    #Redirigir al usuario a la página del dashboard después del login enviando la cookie
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="access_token", value=token, max_age=settings.TOKEN_SECONDS_EXP, path="/")
    return response


#----------------------------------------------------
# 3. Ruta: Dashboard protegido (requiere autenticación)
# ----------------------------------------------------
@router.get("/users/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    access_token: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db)
):
    if not access_token:
        return RedirectResponse(url="/", status_code=303)

    try:
        #Decodificar el token JWT para obtener la información del usuario
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        nick_name: str = payload.get("nick_name")

        user = crud_users.obtener_usuario_por_nickname(db, nick_name)
        if not user:
            return RedirectResponse(url="/", status_code=303)
        
        return templates.TemplateResponse(
            "dashboard.html",
            {"request": request, "nick_name": user.nick_name}
            )
    except JWTError:
        return RedirectResponse(url="/", status_code=303)
    

#----------------------------------------------------
# 4. Ruta: Logout (cerrar sesión)
# ----------------------------------------------------
@router.get("/users/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    # Eliminar la cookie de la sesión del token JWT
    response.delete_cookie(key="access_token", path="/")
    return response

#----------------------------------------------------
# 5. Ruta: Mostrar formulario de registro de usuario
# ----------------------------------------------------  
@router.get("/register", response_class=HTMLResponse)
def mostrar_formulario_registro(request: Request):
    """
    Lo que hace es mostrar la página html del formulario de registro de nuevo usuario.
    """
    return templates.TemplateResponse("register.html", {"request": request})

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
    auth_services.registrar_nuevo_usuario(
        db, nick_name, contrasena, grupo, email
    )

    # Redirigir al usuario al login después del registro
    return RedirectResponse(url="/login", status_code=303)
