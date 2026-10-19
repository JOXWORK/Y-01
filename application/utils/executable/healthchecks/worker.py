import asyncio
import sys

from core.tasks.__worker_healthcheck.get_health_state import GetHealthState


async def main():
    try:
        task = await GetHealthState.kiq()
        task_result = await task.wait_result()
        return_value = task_result.return_value

        if not return_value:
            raise Exception

        sys.exit(0)
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
