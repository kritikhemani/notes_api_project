import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from requests import session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db

TEST_DB_URL = "postgresql+asyncpg://postgres:password@localhost/project_test_db"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
    
@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    yield engine
    await engine.dispose()
        
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
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
        