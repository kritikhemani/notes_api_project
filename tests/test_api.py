import pytest
import pytest_asyncio
from httpx import AsyncClient
from app.main import app

  
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as async_client:
        yield async_client
        
@pytest.mark.asyncio
async def test_register_and_create_note(client):
    # Register user
    response = await client.post("/auth/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201
    token = response.json()["access_token"]
    
    #Create note
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post("/notes/", json={"title": "Test Note", "content": "This is a test note."}, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Note"

@pytest.mark.asyncio
async def test_read_note(client):
    pass

