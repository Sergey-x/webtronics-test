import typing as tp

from database import engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


class BaseCRUD:
    engine: AsyncEngine = engine
    async_session = sessionmaker(engine, class_=AsyncSession)

    @classmethod
    async def execute(cls, statement: tp.Any, values: tp.Union[list[dict], dict, None] = None) -> tp.Any:
        async with cls.engine.begin() as conn:
            return await conn.execute(statement, parameters=values)
