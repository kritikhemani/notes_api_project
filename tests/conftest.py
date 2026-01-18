import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.pool import NullPool
import pytest_asyncio
from alembic import command
from alembic.config import Config
import os

from app.main import app
from app.database import get_db

TEST_DB_URL = "postgresql+asyncpg://postgres:password@localhost/project_test_db"

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
    
@pytest.fixture(scope="session")
def test_engine():
    return create_async_engine(TEST_DB_URL, poolclass=NullPool)

@pytest.fixture(scope="session", autouse=True)
async def db_setup(test_engine):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")
    async with engine.begin() as conn:
        await conn.execute ("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")
    yield
    await engine.dispose()

@pytest_asyncio.fixture(scope="session")
async def client():
    #Use ASGITransport to create an AsyncClient for FastAPI app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as async_client:
        yield async_client