import sqlalchemy as sa

from .base import BaseTable


USERS_TABLE_NAME: str = "users"


class User(BaseTable):
    __tablename__ = USERS_TABLE_NAME

    email = sa.Column(
        sa.VARCHAR(length=320),
        unique=True,
        doc="Электронная почта пользователя",
    )

    password = sa.Column(
        sa.VARCHAR(length=255),
        doc="Пароль пользователя",
    )

    @classmethod
    def get_fields(cls) -> tuple:
        return (
            cls.id,
            cls.email,
        )

    @classmethod
    def get_fields_keys(cls) -> tuple:
        return (
            "id",
            "email",
        )
