import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.Core.config import settings

# ----------------------------------------------------
# 1. Hashear contraseña (de texto plano a hash) 
# ----------------------------------------------------
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()  # Genera un salt aleatorio
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) #Con encode se convierte el string de la contraseña en bytees
    return hashed_password.decode('utf-8') #Convierte la contraseña que fue converitda en bytes a String nuevamente

# ----------------------------------------------------
# 2. Verificar contraseña (comparar texto plano con hash)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# ----------------------------------------------------
# 3. Crear Token JWT
# ----------------------------------------------------
def create_token(data:dict):
    data_token = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=settings.TOKEN_SECONDS_EXP)
    data_token.update({"exp": expire})

    token_jwt = jwt.encode(data_token, settings.SECRET_KEY, algorithm="HS256")
    return token_jwt
 