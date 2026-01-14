import pytest
from httpx import AsyncClient
import pytest_asyncio
from app.main import app
from alembic import command
from alembic.config import Config


TEST_DB_URL = "postgresql+asyncpg://postgres:password@localhost/project_test_db"