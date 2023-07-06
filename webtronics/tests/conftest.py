import asyncio
import os
from types import SimpleNamespace
from uuid import uuid4

import pytest
import pytest_asyncio
from alembic.command import upgrade
from alembic.config import Config
from db.db import MyDatabase
from httpx import AsyncClient
from settings import SETTINGS
from sqlalchemy_utils import create_database, database_exists, drop_database
from tests.utils import make_alembic_config


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates event loop for tests.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    yield loop
    loop.close()


@pytest.fixture
def postgres() -> str:
    """
    Создает временную БД для запуска теста.
    """

    tmp_name = ".".join([uuid4().hex, "pytest"])
    SETTINGS.POSTGRES_DBNAME = tmp_name
    os.environ['POSTGRES_DBNAME'] = tmp_name

    tmp_url = SETTINGS.get_sync_database_uri()
    if not database_exists(tmp_url):
        create_database(tmp_url)

    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


@pytest.fixture
def alembic_config(postgres: str) -> Config:
    """
    Создает файл конфигурации для alembic.
    """
    cmd_options = SimpleNamespace(config="", name="alembic", pg_url=postgres, raiseerr=False, x=None)
    return make_alembic_config(cmd_options)


@pytest.fixture
def migrated_postgres(alembic_config: Config):
    """
    Проводит миграции.
    """
    upgrade(alembic_config, "head")


@pytest_asyncio.fixture
async def async_client(migrated_postgres) -> AsyncClient:
    from main import app as fastapi_app

    MyDatabase.init()  # без вызова метода изменения конфига внутри фикстуры postgres не подтягиваются в класс
    async with AsyncClient(app=fastapi_app, base_url="http://test") as async_test_client:
        yield async_test_client
