import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    reset_test_db()