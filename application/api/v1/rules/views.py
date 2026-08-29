from __future__ import annotations

from typing import TYPE_CHECKING

from core.schemas.moderation_rules import ModerationRulesSchema
from fastapi import APIRouter, Depends

from api.dependencies.auth.fastapi_users_instance import fastapi_current_user

from . import crud
from .schemas import ReadySuccessResponseSchema

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


@router.post("/result/{task_id}")
async def moderation_rules_result(
    task_id: str,
    user: User = Depends(fastapi_current_user),
) -> ReadySuccessResponseSchema:
    result = await crud.get_task_result(task_id)

    return result
