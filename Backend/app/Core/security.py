import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from Backend.app.Core.config import settings

# ----------------------------------------------------
# 1. Hashear contraseña (de texto plano a hash) 
# ----------------------------------------------------
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()  # Genera un salt aleatorio
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) #Con encode se convierte el string de la contraseña en bytees, tipo: b'$2b$12$KIXQJj8uG9Z5e5s1z1e7uO8X9v1y5n6q7r8s9t0u1v2w3x4y5z6' esto 
    return hashed_password.decode('utf-8') #Convierte la contraseña que fue converitda en bytes a String nuevamente, es decir se obtiene un string con el hash de la contraseña, tipo: '$2b$12$KIXQJj8uG9Z5e5s1z1e7uO8X9v1y5n6q7r8s9t0u1v2w3x4y5z6'

# ----------------------------------------------------
# 2. Verificar contraseña (comparar texto plano con hash)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')) 

# ----------------------------------------------------
# 3. Crear Token JWT
# ----------------------------------------------------
def create_token(data:dict):
    data_token = data.copy() # Copia los datos para no modificar el original
    expire = datetime.utcnow() + timedelta(seconds=settings.TOKEN_SECONDS_EXP) # Establece la expiración del token, datetime.utcnow() obtiene la fecha y hora actual en formato UTC, y se le suma el tiempo de expiración definido en la configuración

    token_jwt = jwt.encode(data_token, settings.SECRET_KEY, algorithm="HS256") # Crea el token JWT utilizando la función encode de la biblioteca jose, pasando el payload (data_token), la clave secreta y el algoritmo de encriptación
    return token_jwt
 