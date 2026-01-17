import pytest
import pytest_asyncio
from httpx import AsyncClient
        
@pytest.mark.asyncio
async def test_register_and_create_note(client):
    # Register user
    response = await client.post("/auth/register", json={"name": "Test User", "email": "testuser@example.com", "password": "testpassword123"})
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
    response = await client.post("/auth/register", json={"name": "Test User 2", "email": "testuser2@example.com", "password": "testpassword123"})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    await client.post("/notes/create/", json={"title": "Another Note", "content": "Content here."}, headers=headers)
    response = await client.get("/notes/read/", headers=headers)
    assert response.status_code == 200
    notes = response.json()
    assert len(notes) > 0