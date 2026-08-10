from __future__ import annotations

import orjson
import pytest_asyncio
from httpx import AsyncClient

from .credentials import credentials

url_root = "http://127.0.0.1:8000/api/v1"


@pytest_asyncio.fixture
async def client():
    async with AsyncClient() as client:
        yield client


@pytest_asyncio.fixture
async def register(client: AsyncClient):
    response = await client.post(
        url=url_root + "/auth/register",
        json=credentials["register"],
    )

    print(credentials["register"])

    assert response.status_code == 201


@pytest_asyncio.fixture(scope="session")
async def token_pair(client: AsyncClient):
    response = await client.post(
        url=url_root + "/auth/login",
        data=credentials["login"],
    )

    assert response.status_code == 200

    data = orjson.loads(response.text)

    print(data)

    assert "access_token" in data
    assert "refresh_token" in data

    return data


@pytest_asyncio.fixture
async def first_register_login(register, token_pair):
    pass
