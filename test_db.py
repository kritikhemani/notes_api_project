import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

TEST_DB_URL = "postgresql+asyncpg://postgres:password@localhost/project_test_db"

def create_test_db():
    pass