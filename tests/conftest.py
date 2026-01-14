import pytest
from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    reset_test_db()