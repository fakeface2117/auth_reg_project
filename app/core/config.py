import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# загрузка конфигов из .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../.env'))


class Settings(BaseSettings):
    DRIVER: str = "postgresql+asyncpg"
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASS: int = os.getenv('DB_PASS')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_CONNECTION_STRING: str = f"{DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SECRET_AUTH_KEY: str = os.getenv('SECRET_AUTH_KEY')

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str = "something_secret_key"
    ALGORITHM_HASH: str = "HS256"
    COOKIE_NAME: str = "store"


settings = Settings()
