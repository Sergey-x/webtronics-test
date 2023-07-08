import fastapi as fa

from .v1 import auth_router, post_like_router, post_router


api_router = fa.APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(post_like_router, prefix="/posts", tags=["likes"])
api_router.include_router(post_router, prefix="/posts", tags=["posts"])
