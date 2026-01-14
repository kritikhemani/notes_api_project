import pytest
from httpx import AsyncClient
import pytest_asyncio


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    reset_test_db()