import fastapi as fa
from crud.like import PostLikeCRUD
from fastapi.responses import ORJSONResponse
from fastapi_jwt_auth import AuthJWT


api_router = fa.APIRouter()


@api_router.post(
    "/{post_id}",
    response_class=ORJSONResponse,
    status_code=fa.status.HTTP_201_CREATED,
    responses={
        fa.status.HTTP_201_CREATED: {
            "description": "Ok",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def add_like(
        post_id: int = fa.Path(),
        authorize: AuthJWT = fa.Depends(),
):
    """Добавить лайк к посту с идннтификатором `post_id`."""
    authorize.jwt_required()
    user_id: int = authorize.get_jwt_subject()

    res = await PostLikeCRUD.add_like(post_id=post_id, user_id=user_id)
    if res is None:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
        )


@api_router.delete(
    "/{post_id}",
    response_class=ORJSONResponse,
    status_code=fa.status.HTTP_204_NO_CONTENT,
    responses={
        fa.status.HTTP_201_CREATED: {
            "description": "Ok",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def remove_like(
        post_id: int = fa.Path(),
        authorize: AuthJWT = fa.Depends(),
):
    """Убрать лайк с поста с идннтификатором `post_id`."""
    authorize.jwt_required()
    user_id: int = authorize.get_jwt_subject()

    res = await PostLikeCRUD.remove_like(post_id=post_id, user_id=user_id)
    if res == 0 or res is None:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
        )
