from __future__ import annotations

from typing import TYPE_CHECKING

from core.authentication.rate_limiter import rate_limiter
from fastapi import APIRouter, Depends

from api.dependencies.auth.fastapi_users_instance import fastapi_current_user

if TYPE_CHECKING:
    from core.models.user import User

from . import crud
from .schemas import APITaskResponseSchema

router = APIRouter()


@router.get("/get/{task_id}")
@rate_limiter.restrain(
    kwarg_schema="user.id",
    endpoint_cfg=rate_limiter.config.task_response,
)
async def task_response_get(
    task_id: str,
    user: User = Depends(fastapi_current_user),
) -> APITaskResponseSchema:
    return await crud.get_result(task_id)
