import pytest_asyncio
from core.models.db_attach import db_attach


@pytest_asyncio.fixture
async def session():
    async with db_attach.session_factory() as session:
        yield session
        await db_attach.dispose()
