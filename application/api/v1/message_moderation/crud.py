from core.schemas.moderation_response import ModerationResponseSchema
from core.taskiq.result_backend import result_backend
from core.tasks.message_moderation.send_message_moderation_api import send_message_moderation_api_task
from pydantic import ValidationError

from api.schemas.v1.task_id import TaskIDSchema

from .schemas import ModerationResponseNotReadySchema


async def send_request(message: int, user_id: int) -> TaskIDSchema:
    task = await send_message_moderation_api_task.kiq(
        message=message,
        user_id=user_id,
    )

    return TaskIDSchema(task_id=task.task_id)


async def send_response(task_id: str) -> ModerationResponseSchema | ModerationResponseNotReadySchema | None:
    task_is_ready = await result_backend.is_result_ready(task_id)

    moderation_response = ModerationResponseNotReadySchema()
    if task_is_ready:
        task_result = await result_backend.get_result(task_id)
        return_value = task_result.return_value

        if return_value is None:
            return None

        try:
            moderation_response = ModerationResponseSchema(**return_value)
        except ValidationError:
            pass

    return moderation_response
