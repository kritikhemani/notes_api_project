import pytest
import pytest_asyncio
from httpx import AsyncClient

async def register_and_get_token(client):
    response = await client.post("/auth/register", json={"name": "Test User", "email": "testuser@example.com", "password": "secure123"})
    assert response.status_code == 201
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_register_and_create_note(client):
    # Register user
    response = await client.post("/auth/register", json={"name": "Test User", "email": "testuser@example.com", "password": "secure123"})
    if response.status_code == 422:
        print(response.json())
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
    token = await register_and_get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    await client.post("/notes/", json={"title": "Another Note", "content": "Content here."}, headers=headers)
    response = await client.get("/notes/read/", headers=headers)
    assert response.status_code == 200
    notes = response.json()
    assert len(notes) > 0