import os
from typing import Literal

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


# загрузка конфигов из .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../.env'))


class Settings(BaseSettings):
    MODE: Literal['DEV', 'TEST', 'PROD'] = os.getenv('MODE')

    SERVICE_HOST: str = "localhost"
    SERVICE_PORT: int = 8099

    DRIVER: str = "postgresql+asyncpg"

    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASS: str = os.getenv('DB_PASS')
    DB_NAME: str = os.getenv('DB_NAME')

    @property
    def DB_CONNECTION_STRING(self):
        return f"{self.DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    TEST_DB_HOST: str = os.getenv('TEST_DB_HOST')
    TEST_DB_PORT: int = os.getenv('TEST_DB_PORT')
    TEST_DB_USER: str = os.getenv('TEST_DB_USER')
    TEST_DB_PASS: str = os.getenv('TEST_DB_PASS')
    TEST_DB_NAME: str = os.getenv('TEST_DB_NAME')

    @property
    def DB_CONNECTION_STRING_TEST(self):
        return f"{self.DRIVER}://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    SECRET_AUTH_KEY: str = os.getenv('SECRET_AUTH_KEY')
    ALGORITHM_HASH: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    COOKIE_NAME: str = "access_token"

    MY_EMAIL_ADDRESS: str = os.getenv('MY_EMAIL_ADDRESS')
    MY_EMAIL_PASSWORD: str = os.getenv('MY_EMAIL_PASSWORD')
    MY_SMTP_SERVER: str = 'smtp.mail.ru'

settings = Settings()