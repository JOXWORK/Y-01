from __future__ import annotations

import orjson
import pytest_asyncio
from core.models import db_attach
from httpx import AsyncClient

from .credentials import credentials

url_root = "http://127.0.0.1:8000/api/v1"


@pytest_asyncio.fixture
async def client():
    async with AsyncClient() as client:
        yield client
        await client.aclose()


@pytest_asyncio.fixture
async def session():
    async with db_attach.session_factory() as session:
        yield session
        print("Dispose")
        await db_attach.dispose()


@pytest_asyncio.fixture
async def auth_header(client: AsyncClient):
    response = await client.post(
        url=url_root + "/auth/register",
        json=credentials["register"],
    )

    assert response.status_code == 201

    response = await client.post(
        url=url_root + "/auth/login",
        data=credentials["login"],
    )

    assert response.status_code == 200

    data = orjson.loads(response.text)
    access_token = data["access_token"]

    return {"Authorization": f"Bearer {access_token}"}
