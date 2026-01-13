import pytest
import pytest_asyncio
from httpx import AsyncClient
from app.main import app

  
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as async_client:
        yield async_client