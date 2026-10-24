import asyncio

from core.models.db_attach import db_attach

pytest_plugins = ["tests.testing_core.fixtures"]


async def dispose_engine_hook():
    await db_attach.dispose()


def pytest_sessionfinish(session, exitstatus):
    asyncio.run(dispose_engine_hook())
