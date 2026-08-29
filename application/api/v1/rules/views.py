from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends

from api.dependencies.auth.fastapi_users_instance import fastapi_current_user

from . import crud
from .schemas import ModerationRulesSchema, TaskReadySuccessResult

if TYPE_CHECKING:
    from core.models.user import User

router = APIRouter()


# add rate limit
@router.post("/set")
async def moderation_rules_set(
    rules_schema: ModerationRulesSchema,
    user: User = Depends(fastapi_current_user),
) -> dict[str, str]:
    task_id = await crud.kick_write_rules_task(
        user_id=user.id,
        rules_schema=rules_schema,
    )

    return {"task_id": task_id}


@router.post("/result")
async def moderation_rules_result(
    task_id_schema: str,
    user: User = Depends(fastapi_current_user),
) -> TaskReadySuccessResult:
    result = await crud.get_task_result(task_id=task_id_schema.task_id)

    return result
