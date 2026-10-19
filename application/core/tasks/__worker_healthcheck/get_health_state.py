from core.taskiq.broker import broker


@broker.task
async def GetHealthState() -> bool:
    return True
