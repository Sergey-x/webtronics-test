import time

from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
from log import get_logger
from settings import SETTINGS
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker


logger = get_logger(__name__)


class MyDatabase:
    engine: AsyncEngine | None = None
    SessionLocal = None
    async_session = None
    Base = declarative_base()

    @classmethod
    def init(cls):
        """Set up database.
        Create connection pool.
        """
        if cls.engine is None:
            cls.engine = create_async_engine(SETTINGS.get_async_database_uri(), future=True, pool_size=20,
                                             echo_pool=True)  # noqa
        if cls.SessionLocal is None:
            cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
        if cls.async_session is None:
            cls.async_session = sessionmaker(cls.engine, class_=AsyncSession, expire_on_commit=False)

    @classmethod
    def apply_migrations(cls):
        """Create tables in database if they do not exist."""
        while True:
            try:
                alembic_cfg = AlembicConfig("alembic.ini")
                alembic_command.upgrade(alembic_cfg, "head")
                logger.debug("Migrations created!")
                break
            except BaseException as e:
                logger.error(e)
                logger.error("Try to create tables in 3s...")
                time.sleep(3)

    @classmethod
    async def finish(cls):
        """Dispose the connection pool."""
        if cls.engine is not None:
            await cls.engine.dispose()
            cls.engine = None
            cls.SessionLocal = None
            cls.async_session = None
