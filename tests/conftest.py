import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from alembic import command
from alembic.config import Config
from app.main import app
from app.database import get_db

TEST_DB_URL = "postgresql+asyncpg://postgres:password@localhost/project_test_db"

engine = create_async_engine(TEST_DB_URL, poolclass=NullPool, echo=False)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL.replace("+asyncpg", ""))
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")
    
@pytest.fixture
async def db_session(test_engine):
    async_session = sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)
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
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        yield async_client
        