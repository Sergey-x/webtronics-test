from settings import SETTINGS
from sqlalchemy.ext.asyncio import create_async_engine


engine = create_async_engine(SETTINGS.get_async_database_uri(), pool_size=20)
