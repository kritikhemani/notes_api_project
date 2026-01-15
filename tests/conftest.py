import pytest
from httpx import AsyncClient
import pytest_asyncio
from app.main import app
from alembic import command
from alembic.config import Config


TEST_DB_URL = "postgresql+asyncpg://postgres:password@localhost/project_test_db"

@pytest.fixture(scope="session", autouse=True)
def db_setup():
    alembic_cfg = Config("../alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)
    command.upgrade(alembic_cfg, "head")

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as async_client:
        yield async_client