import os
from functools import lru_cache

import pydantic as pd
from dotenv import load_dotenv
from enums import Stages
from fastapi_jwt_auth import AuthJWT
from log import get_logger


logger = get_logger(__name__)

load_dotenv()


def validate_env_var(varname, v):
    if not v:
        raise ValueError(f"`{varname}` variable is empty")
    return v


class Settings(pd.BaseSettings):
    STAGE: Stages = Stages.PROD
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # ENVS for connecting to postgres
    POSTGRES_DBNAME: str | None
    POSTGRES_USER: str | None
    POSTGRES_PASSWORD: str | None
    POSTGRES_HOST: str | None
    POSTGRES_PORT: int = 5432

    # мимнимальная длина пароля пользователя
    MIN_PSW_LEN: int = 6

    # секрет для генерации JWT
    authjwt_secret_key: str | None = None
    JWT_HEADER: str = "Authorization"

    # ключ доступа для проверки доступности электронной почты пользователя
    NEVERBOUNCE_API_KEY: str | None = None

    @pd.validator("POSTGRES_DBNAME")
    def validate_postgres_dbname_not_empty(cls, v: str):
        return validate_env_var('POSTGRES_DBNAME', v)

    @pd.validator("POSTGRES_USER")
    def validate_chat_postgres_user_not_empty(cls, v: str):
        return validate_env_var('POSTGRES_USER', v)

    @pd.validator("POSTGRES_PASSWORD")
    def validate_postgres_password_not_empty(cls, v: str):
        return validate_env_var('POSTGRES_PASSWORD', v)

    @pd.validator("authjwt_secret_key")
    def validate_authjwt_secret_key_not_empty(cls, v: str):
        return validate_env_var('authjwt_secret_key', v)

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.POSTGRES_DBNAME,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    def get_sync_database_uri(self):
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    def get_async_database_uri(self):
        logger.debug("Use asyncpg driver for db access")
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    class Config:
        env_file = '.env'


@lru_cache
def get_settings() -> Settings:
    return Settings()


@AuthJWT.load_config
def get_config() -> Settings:
    return Settings()


SETTINGS: Settings = get_settings()
