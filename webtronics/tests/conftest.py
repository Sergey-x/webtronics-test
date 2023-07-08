import argparse
import asyncio
import os
from typing import AsyncGenerator, Generator

import pydantic as pd
import pytest
import pytest_asyncio
import services
from alembic import command as alembic_command
from alembic.config import Config
from crud.base import BaseCRUD
from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from httpx import AsyncClient
from requests import Session as RequestSession
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.testclient import TestClient
from tests import utils as test_utils
from tests.common import FACTORIES_SESSION, TEST_SETTINGS
from tests.factories.users import UsersFactory
from tests.mocks import mock_validate_email
from tests.utils import make_alembic_config
from utils.crypto import get_password_hash


services.check_email_deliverable = mock_validate_email


class AuthedUser(pd.BaseModel):
    id: int
    email: str
    password: str
    access_token: str
    refresh_token: str


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates event loop for tests.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    yield loop
    loop.close()


@pytest.fixture(scope="session")
def template_db() -> Generator[str, None, None]:
    with test_utils.tmp_db(db_name=TEST_SETTINGS.POSTGRES_DBNAME, is_template=True) as tmp_name:
        os.environ["POSTGRES_DBNAME"] = tmp_name
        tmp_url = test_utils.build_db_uri(tmp_name)
        alembic_config_ = test_utils.alembic_config_from_url(tmp_url)
        alembic_command.upgrade(alembic_config_, "head")
        yield tmp_name
        os.environ["POSTGRES_DBNAME"] = TEST_SETTINGS.POSTGRES_DBNAME


@pytest.fixture(autouse=True)
def migrated_db(
        template_db: str,
) -> Generator[str, None, None]:
    with test_utils.tmp_db(db_name=TEST_SETTINGS.POSTGRES_DBNAME, from_template=template_db) as tmp_name:
        os.environ["POSTGRES_DBNAME"] = tmp_name
        BaseCRUD.engine = create_async_engine(test_utils.build_db_uri(tmp_name, scheme="postgresql+asyncpg"))
        engine = create_engine(test_utils.build_db_uri(tmp_name))
        FACTORIES_SESSION.configure(bind=engine)
        yield tmp_name
        FACTORIES_SESSION.remove()
        engine.dispose()
        os.environ["POSTGRES_DBNAME"] = TEST_SETTINGS.POSTGRES_DBNAME


@pytest.fixture
def empty_db() -> Generator[str, None, None]:
    with test_utils.tmp_db(db_name=TEST_SETTINGS.POSTGRES_DBNAME) as tmp_name:
        yield test_utils.build_db_uri(tmp_name)


@pytest.fixture
def alembic_config(empty_db: str) -> Config:
    """
    Создает файл конфигурации для alembic.
    """
    cmd_options = argparse.Namespace(
        config="alembic.ini",
        name="alembic",
        pg_url=empty_db,
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options)


@pytest_asyncio.fixture
async def async_client(app: FastAPI, client: TestClient) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=client.base_url) as async_test_client:
        yield async_test_client


@pytest.fixture
def client(app: FastAPI) -> Generator[RequestSession, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def app() -> FastAPI:
    from main import app as fastapi_app

    return fastapi_app


@pytest.fixture
def user_access_token() -> tuple:
    user = UsersFactory.add(1, "firstname.secondname@domain.com", get_password_hash("password"))
    access_token = AuthJWT().create_access_token(subject=1)
    return user, access_token


@pytest.fixture
def authed_user() -> AuthedUser:
    user = UsersFactory.add(
        user_id=1,
        email="firstname.secondname@domain.com",
        password=get_password_hash("password"),
    )
    access_token = AuthJWT().create_access_token(subject=1)
    refresh_token = AuthJWT().create_refresh_token(subject=1)

    user.update({"access_token": access_token, "refresh_token": refresh_token})
    return AuthedUser.parse_obj(user)


def make_auth_header(token: str) -> dict:
    headers = {
        TEST_SETTINGS.JWT_HEADER: f"Bearer {token}",
    }
    return headers
