import asyncio

import pytest
from core.models.db_attach import db_attach

pytest_plugins = ["tests.testing_core.fixtures"]

pytest.register_assert_rewrite("tests.testing_core.additional_checks")


async def dispose_engine_hook():
    await db_attach.dispose()


def pytest_sessionfinish(session, exitstatus):
    asyncio.run(dispose_engine_hook())
