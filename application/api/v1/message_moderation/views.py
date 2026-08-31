from __future__ import annotations

from typing import TYPE_CHECKING

from core.authentication.rate_limiter import rate_limiter
from core.schemas.moderation_response import ModerationResponseSchema
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from api.dependencies.auth.fastapi_users_instance import fastapi_current_user
from api.schemas.v1.task_id import TaskIDSchema

from . import crud
from .schemas import ModerationResponseNotReadySchema

if TYPE_CHECKING:
    from core.models.user import User
router = APIRouter()


@router.post("/send-request")
@rate_limiter.restrain(
    kwarg_schema="user.id",
    endpoint_cfg=rate_limiter.config.message_moderation_request,
)
async def message_moderation_send_request(
    message: str,
    user: User = Depends(fastapi_current_user),
) -> TaskIDSchema:
    return await crud.send_request(
        message=message,
        user_id=user.id,
    )


@router.get("/send-response/{task_id}")
@rate_limiter.restrain(
    kwarg_schema="user.id",
    endpoint_cfg=rate_limiter.config.message_moderation_response,
)
async def message_moderation_send_response(
    task_id: str,
    user: User = Depends(fastapi_current_user),
) -> ModerationResponseSchema | ModerationResponseNotReadySchema:
    moderation_response = await crud.send_response(task_id)

    if moderation_response is None:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)

    return moderation_response
