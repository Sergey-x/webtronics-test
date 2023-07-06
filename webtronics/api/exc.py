import fastapi as fa
from fastapi.responses import ORJSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException


def authjwt_exception_handler(request: fa.Request, exc: AuthJWTException):
    """Exception handler for authjwt"""
    return ORJSONResponse(
        status_code=fa.status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Unauthorized"}
    )


def validation_exception_handler(request: fa.Request, exc):
    """Exception handler for pydantic validation errors"""
    return ORJSONResponse(
        status_code=fa.status.HTTP_400_BAD_REQUEST,
        content={"detail": "Bad request"}
    )
