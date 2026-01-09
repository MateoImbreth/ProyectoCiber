import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY : str = os.environ.get("SECRET_KEY")
    TOKEN_SECONDS_EXP: int = 20
    DATABASE_URL: str = os.environ.get("DATABASE_URL")

settings = Settings()