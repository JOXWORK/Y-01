import orjson
import pytest_asyncio
from httpx import AsyncClient
from tests.test_depends import test_depends


@pytest_asyncio.fixture
async def auth_header(httpx_client: AsyncClient):
    response = await httpx_client.post(
        url=test_depends.urls.endpoint("/auth/register"),
        json=test_depends.user_credentials.register,
    )

    assert response.status_code == 201

    response = await httpx_client.post(
        url=test_depends.urls.endpoint("/auth/login"),
        data=test_depends.user_credentials.login,
    )

    assert response.status_code == 200

    data = orjson.loads(response.text)
    access_token = data["access_token"]

    return {"Authorization": f"Bearer {access_token}"}
