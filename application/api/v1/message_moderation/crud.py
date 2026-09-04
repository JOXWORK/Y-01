from core.tasks.message_moderation.send_message_moderation_api import send_message_moderation_api_task

from api.schemas.v1.task_id import TaskIDSchema


async def send_message_request(message: int, user_id: int) -> TaskIDSchema:
    task = await send_message_moderation_api_task.kiq(
        message=message,
        user_id=user_id,
    )

    return TaskIDSchema(task_id=task.task_id)
