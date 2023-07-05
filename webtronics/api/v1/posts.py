from typing import Annotated

import fastapi as fa
from api.deps import get_db
from crud import PostCRUD
from fastapi.responses import ORJSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_pagination import Page
from pagination import PostPaginationParams
from schemas import CreatePostRequestSchema, PostResponseItem, UpdatePostRequestSchema
from sqlalchemy.ext.asyncio import AsyncSession


api_router = fa.APIRouter()


@api_router.get(
    "/{post_id}",
    response_class=ORJSONResponse,
    response_model=PostResponseItem,
    status_code=fa.status.HTTP_200_OK,
    responses={
        fa.status.HTTP_200_OK: {
            "description": "Ok",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
        fa.status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
        },
    },
)
async def get_post_by_id(
        post_id: Annotated[int, fa.Path()],
        authorize: AuthJWT = fa.Depends(),
        db: AsyncSession = fa.Depends(get_db),
):
    """Получить пост с идентификатором `post_id`."""
    post = await PostCRUD.get_post_by_id(db=db, post_id=post_id)

    if post is None:
        raise fa.HTTPException(status_code=fa.status.HTTP_404_NOT_FOUND)
    return post


@api_router.get(
    "",
    response_class=ORJSONResponse,
    response_model=Page[object],
    status_code=fa.status.HTTP_200_OK,
    responses={
        fa.status.HTTP_200_OK: {
            "description": "Ok",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
        fa.status.HTTP_400_BAD_REQUEST: {
            "description": "Bad request",
        },
    },
)
async def get_recent_posts(
        db: AsyncSession = fa.Depends(get_db),
        params: PostPaginationParams = fa.Depends(),  # noqa
):
    """Возвращает несколько последних постов, по умолчанию - 50. Есть пагинация."""
    posts = await PostCRUD.get_recent_posts(db=db)

    if not posts:
        raise fa.HTTPException(status_code=fa.status.HTTP_400_BAD_REQUEST)
    return posts


@api_router.patch(
    "/{post_id}",
    response_class=ORJSONResponse,
    response_model=PostResponseItem,
    status_code=fa.status.HTTP_200_OK,
    responses={
        fa.status.HTTP_200_OK: {
            "description": "Ok",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def update_message(
        post_id: int,
        post: UpdatePostRequestSchema,
        authorize: AuthJWT = fa.Depends(),
        db: AsyncSession = fa.Depends(get_db),
) -> PostResponseItem:
    """Изменить пост с идентификатором `post_id`."""
    authorize.jwt_required()
    user_id: int = authorize.get_jwt_subject()
    updated_post: PostResponseItem | None = await PostCRUD.update_post(db=db, post_id=post_id, updated_post=post,
                                                                       author_id=user_id)
    if updated_post is None:
        raise fa.HTTPException(fa.status.HTTP_400_BAD_REQUEST)
    return updated_post


@api_router.post(
    "",
    response_class=ORJSONResponse,
    response_model=PostResponseItem,
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
async def add_message(
        authorize: AuthJWT = fa.Depends(),
        post: CreatePostRequestSchema = fa.Body(),
        db: AsyncSession = fa.Depends(get_db),
) -> PostResponseItem:
    """Создать пост."""
    authorize.jwt_required()

    user_id: int = authorize.get_jwt_subject()
    created_post: PostResponseItem | None = await PostCRUD.create_post(db=db, new_post_data=post, author_id=user_id)

    if created_post is None:
        raise fa.HTTPException(fa.status.HTTP_400_BAD_REQUEST)
    return created_post


@api_router.delete(
    "/{post_id}",
    status_code=fa.status.HTTP_204_NO_CONTENT,
    responses={
        fa.status.HTTP_204_NO_CONTENT: {
            "description": "Ok",
        },
        fa.status.HTTP_400_BAD_REQUEST: {
            "description": "Bad message id",
        },
        fa.status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def soft_delete_post(
        post_id: int,
        authorize: AuthJWT = fa.Depends(),
        db: AsyncSession = fa.Depends(get_db),
):
    """Удалить пост с идентификатором `post_id`."""
    authorize.jwt_required()
    user_id: int = authorize.get_jwt_subject()

    deleted_row: int = await PostCRUD.delete_post(db=db, post_id=post_id, author_id=user_id)
    if deleted_row == 0:
        raise fa.HTTPException(status_code=fa.status.HTTP_400_BAD_REQUEST, detail="Нет указанного объекта")
