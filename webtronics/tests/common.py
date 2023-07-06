from settings.settings import get_settings
from sqlalchemy import orm


TEST_SETTINGS = get_settings()
TEST_SETTINGS.POSTGRES_DBNAME = "testdb"
ALEMBIC_PATH = TEST_SETTINGS.PROJECT_ROOT
FACTORIES_SESSION = orm.scoped_session(orm.sessionmaker())
