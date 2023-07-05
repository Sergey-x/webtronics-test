import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.sql import func

from .base import BaseTable
from .user import User


POSTS_TABLE_NAME: str = "posts"


class Post(BaseTable):
    __tablename__ = POSTS_TABLE_NAME

    dt_created = sa.Column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
        index=True,
        doc="Дата и время создания (type TIMESTAMP)",
    )

    dt_updated = sa.Column(
        TIMESTAMP(timezone=True),
        nullable=True,
        doc="Дата и время обновления (type TIMESTAMP)",
    )

    text = sa.Column(
        sa.Text,
        nullable=False,
        doc="Контент",
    )

    is_available = sa.Column(
        sa.Boolean,
        nullable=False,
        default=True,
        doc='Удалено автором или нет',
    )

    author_id = sa.Column(
        sa.ForeignKey(User.id),  # noqa
        doc="Идентификтор автора post",
    )

    likes = sa.Column(
        sa.INTEGER,
        default=0,
        nullable=False,
        doc="Количество лайков",
    )

    @classmethod
    def get_post_fields(cls) -> tuple:
        return (
            cls.id,
            cls.text,
            cls.dt_created,
            cls.dt_updated,
            cls.is_available,
            cls.author_id,
            cls.likes,
        )

    @classmethod
    def get_post_fields_keys(cls) -> tuple:
        return (
            "id",
            "text",
            "dt_created",
            "dt_updated",
            "is_available",
            "author_id",
            "likes",
        )
