from __future__ import annotations

from typing import TYPE_CHECKING

from core.authentication.rate_limiter import rate_limiter
from fastapi import (
    APIRouter,
    Depends,
)

from api.dependencies.auth.fastapi_users_instance import fastapi_current_user
from api.schemas.v1.task_id import TaskIDSchema

from . import crud

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
