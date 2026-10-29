import asyncio

import pytest_asyncio


@pytest_asyncio.fixture(scope="function", loop_scope="class")
async def func_class__async_delay(request):
    marker = request.node.get_closest_marker("delay")
    delay = 2
    if marker:
        delay = marker.args[0]
    yield delay

    await asyncio.sleep(delay)
