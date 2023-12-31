import sqlalchemy as sa
from database import DeclarativeBase


class BaseTable(DeclarativeBase):
    __abstract__ = True

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        doc="Unique index of element",
    )
