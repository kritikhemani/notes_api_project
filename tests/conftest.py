import pytest
from httpx import AsyncClient
import pytest_asyncio
from app.main import app
from alembic import command
from alembic.config import Config


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    reset_test_db()