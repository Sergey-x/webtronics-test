from .auth import api_router as auth_router
from .post_like import api_router as post_like_router
from .posts import api_router as post_router


__all__ = (
    "auth_router",
    "post_router",
    "post_like_router",
)
