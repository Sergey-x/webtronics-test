import fastapi as fa
from crud.auth import AuthCRUD
from fastapi.responses import ORJSONResponse
from fastapi_jwt_auth import AuthJWT
from schemas.auth import JWTPair, SignInRequestSchema, SignUpRequestSchema
from services import check_email_deliverable


api_router = fa.APIRouter()


def get_jwt_pair(authorize, subject: int) -> JWTPair:
    """Генерирует пару токенов (access, refresh) на основании `subject`.

    Возвращает в виде модели JWTPair.
    """
    access_token = authorize.create_access_token(subject=subject)
    refresh_token = authorize.create_refresh_token(subject=subject)
    tokens: JWTPair = JWTPair(access_token=access_token, refresh_token=refresh_token)
    return tokens


@api_router.post(
    "/signup",
    response_class=ORJSONResponse,
    response_model=JWTPair,
    status_code=fa.status.HTTP_201_CREATED,
    responses={
        fa.status.HTTP_201_CREATED: {
            "description": "Successfully registered",
        },
        fa.status.HTTP_400_BAD_REQUEST: {
            "description": "Bad request",
        },
        fa.status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error",
        },
    },
)
async def sign_up(

        authorize: AuthJWT = fa.Depends(),
        user_creds: SignUpRequestSchema = fa.Body(),
) -> JWTPair:
    """Зарегистрироваться по почте и паролю.

    При успешной регистрации пользователь получает пару токенов.
    """
    authorize.jwt_optional()

    # Проверяем, что email корректен на стороннем сервисе
    is_email_valid: bool = await check_email_deliverable(user_creds.email)
    if not is_email_valid:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Invalid email address, use another",
        )

    new_user_id: int | None = await AuthCRUD.sign_up(user_creds=user_creds)
    if new_user_id is None:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Creating user error",
        )

    tokens: JWTPair = get_jwt_pair(authorize=authorize, subject=new_user_id)
    return tokens


@api_router.post(
    "/signin",
    response_class=ORJSONResponse,
    response_model=JWTPair,
    status_code=fa.status.HTTP_200_OK,
    responses={
        fa.status.HTTP_200_OK: {
            "description": "Ok",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
        fa.status.HTTP_400_BAD_REQUEST: {
            "description": "Not found",
        },
    },
)
async def sign_in(
        authorize: AuthJWT = fa.Depends(),
        user_creds: SignInRequestSchema = fa.Body(),
) -> JWTPair:
    """Вход по почте и паролю.

    Пользователь получает пару токенов.
    """

    # получаем пользователя по имени и паролю
    user_id: int | None = await AuthCRUD.get_user_id_by_creds(user_creds=user_creds)

    if user_id is None:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Ошибка ввода логина или пароля",
        )

    tokens: JWTPair = get_jwt_pair(authorize=authorize, subject=user_id)
    return tokens


@api_router.post(
    "/refresh",
    response_class=ORJSONResponse,
    response_model=JWTPair,
    status_code=fa.status.HTTP_200_OK,
    responses={
        fa.status.HTTP_200_OK: {
            "description": "Ok",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
        fa.status.HTTP_400_BAD_REQUEST: {
            "description": "Not found",
        },
    },
)
async def refresh(
        authorize: AuthJWT = fa.Depends(),
) -> JWTPair:
    """Обновление JWT.

    Для обновления в http заголовке Authorization должен быть токен типа refresh.
    """
    authorize.jwt_refresh_token_required()

    current_subject = authorize.get_jwt_subject()

    tokens: JWTPair = get_jwt_pair(authorize=authorize, subject=current_subject)
    return tokens
