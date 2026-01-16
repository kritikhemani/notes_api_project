import pytest
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
from app.main import app
from alembic import command
from alembic.config import Config
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

TEST_DB_URL = "postgresql+asyncpg://postgres:password@localhost/project_test_db"

@pytest.fixture(scope="session", autouse=True)
def db_setup():
    alembic_path = os.path.join(os.path.dirname(__file__), "../alembic.ini")
    alembic_cfg = Config(alembic_path)
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")

@pytest_asyncio.fixture
async def client():
    #Use ASGITransport to create an AsyncClient for FastAPI app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as async_client:
        yield async_client