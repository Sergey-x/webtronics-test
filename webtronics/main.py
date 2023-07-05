import fastapi as fa
from api import api_router
from api.v1.auth import authjwt_exception_handler
from enums import Stages
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_pagination import add_pagination
from settings import SETTINGS


SWAGGER_PATH = "/swagger"
OPENAPI_PATH = "/openapi"


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

    application.add_exception_handler(AuthJWTException, authjwt_exception_handler)

    return application


app = get_app()
