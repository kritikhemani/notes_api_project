import pytest
from test_db import TEST_DB_URL
import pytest_asyncio
from httpx import AsyncClient
from app.main import app
from alembic.config import Config
from alembic import command

alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    pass