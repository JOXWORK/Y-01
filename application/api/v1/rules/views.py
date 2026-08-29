from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends

from api.dependencies.auth.fastapi_users_instance import fastapi_current_user

from .crud import execute_write_moderation_rules_task, get_result_moderation_rules_task
from .schemas import ModerationRulesSchema, TaskIDSchema, TaskResult

if TYPE_CHECKING:
    from core.models.user import User

router = APIRouter()


# add rate limit
@router.post("/set")
async def moderation_rules_set(
    rules_schema: ModerationRulesSchema,
    user: User = Depends(fastapi_current_user),
) -> TaskIDSchema:
    task_id = await execute_write_moderation_rules_task(
        user_id=user.id,
        rules_schema=rules_schema,
    )

    return TaskIDSchema(task_id=task_id)


@router.post("/result")
async def moderation_rules_result(
    task_id_schema: TaskIDSchema,
    user: User = Depends(fastapi_current_user),
) -> TaskResult:
    result = await get_result_moderation_rules_task(task_id=task_id_schema.task_id)

    return TaskResult(**result)
