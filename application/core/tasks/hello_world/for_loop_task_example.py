from core.taskiq import broker


@broker.task
async def for_loop_task_example_task(stop: int) -> int:
    for i in range(stop):
        if i == stop - 1:
            return i
