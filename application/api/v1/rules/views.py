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


@router.post("/set-request")
@rate_limiter.restrain(
    kwarg_schema="user.id",
    endpoint_cfg=rate_limiter.config.common_moderation_rules_request,
)
async def moderation_rules_set_request(
    rules_schema: ModerationRulesSchema,
    user: User = Depends(fastapi_current_user),
) -> TaskIDSchema:
    return await crud.set_request(
        user_id=user.id,
        rules_schema=rules_schema,
    )


@router.post("/get-request")
@rate_limiter.restrain(
    kwarg_schema="user.id",
    endpoint_cfg=rate_limiter.config.common_moderation_rules_request,
)
async def moderation_rules_get_request(
    user: User = Depends(fastapi_current_user),
) -> TaskIDSchema:
    return await crud.get_request(user.id)
