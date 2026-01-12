import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import command
from alembic.config import Config
from app.database import Base

TEST_DB_URL = "postgresql+asyncpg://postgres:password@localhost/project_test_db"

def create_test_db():
    engine = create_async_engine(TEST_DB_URL)
    asyncio.run(engine.run_sync(Base.metadata.create_all))
    
alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)
    
def run_migrations():
    command.upgrade(alembic_cfg, "head")

def reset_test_db():
    pass