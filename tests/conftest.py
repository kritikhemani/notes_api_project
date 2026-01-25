import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from sqlalchemy.pool import NullPool
import pytest_asyncio
from alembic import command
from alembic.config import Config
from app.main import app
from app.database import get_db

TEST_DB_URL = "postgresql+asyncpg://postgres:password@localhost/project_test_db"
   
@pytest.fixture(scope="session")
def test_engine():
    engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
    yield engine
    asyncio.run(engine.dispose())

@pytest.fixture(scope="session", autouse=True)
async def run_migrations(test_engine):
    alembic_cfg = Config("alembic.ini")
    
    async with test_engine.begin() as conn:
        await conn.run_sync(lambda _: command.upgrade(alembic_cfg, "head"))
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(lambda _: command.downgrade(alembic_cfg, "base"))
    
@pytest.fixture
async def db_session(test_engine):
    async_session = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)
    
    async with test_engine.begin() as conn:
        trans = await conn.begin_nested()

    async with async_session() as session:
        yield session
        await session.rollback()
        
@pytest.fixture(autouse=True)
def override_get_db(db_session):
    async def _override():
        yield db_session
    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()
        
@pytest.fixture(scope="session")
async def client():
    #Use ASGITransport to create an AsyncClient for FastAPI app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as async_client:
        yield async_client
        