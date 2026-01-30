import pytest
from httpx import AsyncClient
from uuid import uuid4

def random_email():
    return f"user_{uuid4().hex[:8]}@example.com"


async def register(client: AsyncClient, email: str, password: str):
    r = await client.post(
        "/auth/register",
        json={"name": "Test User", "email": email, "password": password},
    )
    assert r.status_code == 200


async def login(client: AsyncClient, email: str, password: str) -> str:
    r = await client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )
    assert r.status_code == 200
    return r.json()["access_token"]


@pytest.mark.asyncio
async def test_register_and_create_note(client: AsyncClient):
    email = random_email()
    password = "secure123"

    await register(client, email, password)
    token = await login(client, email, password)

    headers = {"Authorization": f"Bearer {token}"}

    r = await client.post(
        "/notes/create/",
        json={"title": "Test Note", "content": "This is a test"},
        headers=headers,
    )

    assert r.status_code == 200
    assert r.json()["title"] == "Test Note"


@pytest.mark.asyncio
async def test_read_note(client: AsyncClient):
    email = random_email()
    password = "secure123"

    await register(client, email, password)
    token = await login(client, email, password)

    headers = {"Authorization": f"Bearer {token}"}

    await client.post(
        "/notes/create/",
        json={"title": "Another Note", "content": "Hello"},
        headers=headers,
    )

    r = await client.get("/notes/read/", headers=headers)

    assert r.status_code == 200
    assert len(r.json()) > 0
