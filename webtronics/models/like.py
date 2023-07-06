import sqlalchemy as sa
from database import DeclarativeBase

from .post import Post
from .user import User


LIKES_TABLE_NAME: str = "likes"


class PostLike(DeclarativeBase):
    __tablename__ = LIKES_TABLE_NAME

    post_id = sa.Column(
        sa.ForeignKey(Post.id),  # noqa
        primary_key=True,
        doc="Идентификатор post, которому поставили лайк",
    )
    user_id = sa.Column(
        sa.ForeignKey(User.id),  # noqa
        primary_key=True,
        doc="Идентификатор пользователя, который поставил лайк",
    )

    @classmethod
    def get_post_like_fields(cls) -> tuple:
        return (
            cls.post_id,
            cls.user_id,
        )

    @classmethod
    def get_post_like_fields_keys(cls) -> tuple:
        return (
            "post_id",
            "user_id",
        )
