# /backend/app/services/mfa_service.py

import pyotp
import qrcode # Librería útil para generar la imagen del QR

# ----------------------------------------------------
# Lógica de Generación de la Clave Secreta y el QR
# ----------------------------------------------------

def generate_mfa_secret() -> str:
    """Genera una nueva clave secreta base32 aleatoria (seed) para un usuario."""
    # pyotp.random_base32() genera una clave segura de 16 caracteres.
    return pyotp.random_base32()

def generate_qr_uri(email: str, secret: str, issuer: str = "MFA Portal API") -> str:
    """
    Genera el URI de aprovisionamiento de TOTP.
    Este URI se utiliza para generar el Código QR que el usuario escaneará.
    """
    # El URI sigue el estándar para ser leído por Google Authenticator, Authy, etc.
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=email,
        issuer_name=issuer
    )

def generate_qr_code_image(uri: str) -> bytes:
    """
    Genera el código QR como una imagen (en formato bytes) a partir del URI.
    El frontend de React lo recibirá y mostrará.
    """
    img = qrcode.make(uri)
    import io
    # Guardar la imagen en un buffer de bytes para enviarla directamente a FastAPI
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

# ----------------------------------------------------
# Lógica de Verificación del Token OTP
# ----------------------------------------------------

def verify_otp_token(secret: str, token: str) -> bool:
    """
    Verifica si el token OTP ingresado por el usuario es válido en el tiempo actual.
    
    :param secret: La clave secreta (mfa_secret) guardada para el usuario.
    :param token: El código de 6 dígitos ingresado por el usuario.
    :return: True si el token es válido, False en caso contrario.
    """
    totp = pyotp.TOTP(secret)
    # El método verify() comprueba la validez del token dentro de una ventana de tiempo.
    return totp.verify(token)