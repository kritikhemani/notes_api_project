import pytest
import asyncio
from httpx import AsyncClient
from requests import session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from app.main import app
from app.database import get_db

TEST_DB_URL = "postgresql+asyncpg://postgres:password@localhost/project_test_db"

engine = create_async_engine(TEST_DB_URL, echo=False)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False)

        
@pytest.fixture(autouse=True)
async def override_get_db():
    async def _override():
        async with AsyncSessionLocal() as session:
            yield session
    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()
        
@pytest.fixture(scope="session")
async def client():
    #Use ASGITransport to create an AsyncClient for FastAPI app
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client
        