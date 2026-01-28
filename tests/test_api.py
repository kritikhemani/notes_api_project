import pytest
from httpx import AsyncClient
import uuid

def unique_email() -> str:
    return f"user_{uuid.uuid4().hex}@example.com"

async def register_and_get_token(client: AsyncClient) -> str:
    email = unique_email()
    response = await client.post("/auth/register", json={"name": "Test User", "email": email, "password": "secure123"})
    assert response.status_code == 201
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_register_and_create_note(client: AsyncClient):
    token = await register_and_get_token(client)
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