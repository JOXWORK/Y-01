from core.tasks.message_moderation.send_message_moderation import SendMessageModeration

from api.schemas.v1.task_id import TaskIDSchema


async def send_message(message: int, user_id: int) -> TaskIDSchema:
    task = await SendMessageModeration.kiq(
        message=message,
        user_id=user_id,
    )

    return TaskIDSchema(task_id=task.task_id)
