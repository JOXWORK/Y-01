from __future__ import annotations

from typing import TYPE_CHECKING

from core.authentication.rate_limiter import rate_limiter
from core.schemas.moderation_rules import ModerationRulesSchema
from fastapi import APIRouter, Depends

from api.dependencies.auth.fastapi_users_instance import fastapi_current_user
from api.schemas.v1.task_id import TaskIDSchema

from . import crud

if TYPE_CHECKING:
    from core.models.user import User

router = APIRouter()


@router.post("/create")
@rate_limiter.restrain(
    kwarg_schema="user.id",
    endpoint_cfg=rate_limiter.config.moderation_rules_create,
)
async def moderation_rules_create(
    rules_schema: ModerationRulesSchema,
    user: User = Depends(fastapi_current_user),
) -> TaskIDSchema:
    return await crud.create_rules(
        user_id=user.id,
        rules=rules_schema.model_dump(),
    )


@router.post("/get")
@rate_limiter.restrain(
    kwarg_schema="user.id",
    endpoint_cfg=rate_limiter.config.moderation_rules_get,
)
async def moderation_rules_get(
    user: User = Depends(fastapi_current_user),
) -> TaskIDSchema:
    return await crud.get_rules(user.id)


@router.delete("/delete")
async def moderation_rules_delete(user: User = Depends(fastapi_current_user)) -> TaskIDSchema:
    return await crud.delete_rules(user.id)
