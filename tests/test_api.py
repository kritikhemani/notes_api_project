import pytest
import pytest_asyncio
from httpx import AsyncClient
from app.main import app


    
@pytest_asyncio.fixture
async def client():
    pass