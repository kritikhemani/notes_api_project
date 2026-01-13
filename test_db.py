import asyncio
from alembic import command
from alembic.config import Config

TEST_DB_URL = "postgresql+asyncpg://postgres:password@localhost/project_test_db"

alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)

def create_test_db():
    engine = create_async_engine(TEST_DB_URL)
    asyncio.run(engine.run_sync(Base.metadata.create_all))
    
    
def run_migrations():
    command.upgrade(alembic_cfg, "head")

def reset_test_db():
    command.downgrade(alembic_cfg, "base")
    run_migrations()