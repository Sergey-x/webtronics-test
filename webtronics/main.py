import fastapi as fa
from alembic import command
from api import api_router
from api.exc import authjwt_exception_handler, validation_exception_handler
from enums import Stages
from fastapi.exceptions import RequestValidationError
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_pagination import add_pagination
from settings import SETTINGS
from tests.utils import alembic_config_from_url


SWAGGER_PATH = "/swagger"
OPENAPI_PATH = "/openapi"


def make_migrations():
    alembic_config = alembic_config_from_url(SETTINGS.get_sync_database_uri())
    command.upgrade(alembic_config, "head")


def get_app() -> fa.FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Тестовое для Webtronics."

    application = fa.FastAPI(
        title="Webtronics",
        description=description,
        docs_url=None if SETTINGS.STAGE == Stages.PROD else SWAGGER_PATH,
        openapi_url=None if SETTINGS.STAGE == Stages.PROD else OPENAPI_PATH,
        version="0.1.0",
    )

    # подключение api handlers
    application.include_router(api_router)

    # добавление возможности пагинации
    add_pagination(application)
    application.add_event_handler("startup", make_migrations)

    application.add_exception_handler(AuthJWTException, authjwt_exception_handler)
    application.add_exception_handler(RequestValidationError, validation_exception_handler)

    return application


app = get_app()
