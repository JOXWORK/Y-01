import pytest_asyncio
from core.models.db_attach import db_attach


@pytest_asyncio.fixture(scope="class", loop_scope="class", autouse=True)
async def class_dispose_engine():
    yield

    await db_attach.dispose()
