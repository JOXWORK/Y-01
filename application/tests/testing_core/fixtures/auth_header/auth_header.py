from __future__ import annotations

from typing import TYPE_CHECKING

import orjson
import pytest_asyncio

from tests.testing_core.test_depends import test_depends

if TYPE_CHECKING:
    from httpx import AsyncClient
    from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture(scope="class", loop_scope="class")
async def class_db_auth_header(class_create_db_user: AsyncSession, class_httpx_client: AsyncClient):
    response = await class_httpx_client.post(
        url=test_depends.urls.endpoint("/auth/login"),
        data=test_depends.user_credentials.login,
    )

    assert response.status_code == 200

    data = orjson.loads(response.text)
    access_token = data["access_token"]

    return {"Authorization": f"Bearer {access_token}"}
