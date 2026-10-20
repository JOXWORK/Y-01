from __future__ import annotations

import orjson
import pytest_asyncio
from core.models import db_attach
from httpx import AsyncClient

from .test_depends import test_depends


@pytest_asyncio.fixture
async def client():
    async with AsyncClient() as client:
        yield client
        await client.aclose()


@pytest_asyncio.fixture
async def session():
    async with db_attach.session_factory() as session:
        yield session
        await db_attach.dispose()


@pytest_asyncio.fixture
async def auth_header(client: AsyncClient):
    response = await client.post(
        url=test_depends.urls.endpoint("/auth/register"),
        json=test_depends.user_credentials.register,
    )

    assert response.status_code == 201

    response = await client.post(
        url=test_depends.urls.endpoint("/auth/login"),
        data=test_depends.user_credentials.login,
    )

    assert response.status_code == 200

    data = orjson.loads(response.text)
    access_token = data["access_token"]

    return {"Authorization": f"Bearer {access_token}"}
