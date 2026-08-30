from core.schemas.moderation_rules import ModerationRulesSchema
from core.taskiq.result_backend import result_backend
from core.tasks.moderation_rules.get_moderation_rules_db import get_moderation_rules_db_task
from core.tasks.moderation_rules.set_moderation_rules_db import set_moderation_rules_db_task
from pydantic import ValidationError

from .schemas import GetResponseSchema, SetResponseSchema


async def set_request(user_id: int, rules_schema: ModerationRulesSchema) -> str:
    task = await set_moderation_rules_db_task.kiq(
        user_id=user_id,
        rules_schema=rules_schema,
    )

    return task.task_id


async def set_response(task_id: str) -> SetResponseSchema:
    task_is_ready = await result_backend.is_result_ready(task_id)

    successful = False
    if task_is_ready:
        task_result = await result_backend.get_result(task_id)
        successful = task_result.return_value or False

    if type(successful) is not bool:
        return None

    return SetResponseSchema(
        is_ready=task_is_ready,
        successful=successful,
    )


async def get_request(user_id: int) -> str:
    task = await get_moderation_rules_db_task.kiq(user_id)

    return task.task_id


async def get_response(task_id: int) -> GetResponseSchema:
    task_is_ready = await result_backend.is_result_ready(task_id)

    response_schema = GetResponseSchema(is_ready=task_is_ready, rules=None)

    if task_is_ready:
        task_result = await result_backend.get_result(task_id)
        return_value: dict = task_result.return_value

        try:
            if type(return_value) is not dict:
                return None

            response_schema.rules = return_value.get("rules", {})
        except ValidationError:
            return None

    return response_schema
