import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture(scope="class", loop_scope="class")
async def class_httpx_client():
    async with AsyncClient() as client:
        yield client
        await client.aclose()
