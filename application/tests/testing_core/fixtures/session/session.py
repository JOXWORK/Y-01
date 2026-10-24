import pytest_asyncio
from core.models.db_attach import db_attach


@pytest_asyncio.fixture(scope="class", loop_scope="class")
async def class_session():
    async with db_attach.session_factory() as session:
        yield session
