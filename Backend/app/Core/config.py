import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY : str = os.environ.get("SECRET_KEY")
    TOKEN_SECONDS_EXP: int = 2000

    DB_USER: str = os.environ.get("DB_USER")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD")
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: str = os.environ.get("DB_PORT")
    DB_NAME: str = os.environ.get("DB_NAME")

    DATABASE_URL: str = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
settings = Settings()