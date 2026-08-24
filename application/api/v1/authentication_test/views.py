from __future__ import annotations

from typing import TYPE_CHECKING

from core.authentication.rate_limit_guard import rate_limit_guard
from fastapi import APIRouter, Depends

from api.dependencies.auth import fastapi_current_user

if TYPE_CHECKING:
    from core.models.user import User

from .schemas import BaseCredentialsSchema

router = APIRouter()


@router.get("/is-user-valid")
async def is_user_valid(user: User = Depends(fastapi_current_user)):
    return {"is_valid": True}


@router.post("/rate-limit")
@rate_limit_guard.keep_limit(
    kwarg_schema="user.id",
    endpoint_cfg=rate_limit_guard.config.rate_limit,
)
async def rate_limit(user: User = Depends(fastapi_current_user)):
    return {"message": "succsessful"}


@router.post("/user-email-rate-limit")
@rate_limit_guard.keep_limit(
    kwarg_schema="user.email",
    endpoint_cfg=rate_limit_guard.config.user_email_rate_limit,
)
async def user_email_rate_limit(user: User = Depends(fastapi_current_user)):
    return {"successful": True}


@router.post("/pydantic-schema-rate-limit")
@rate_limit_guard.keep_limit(
    kwarg_schema="base_credentials.email",
    endpoint_cfg=rate_limit_guard.config.pydantic_schema_rate_limit,
)
async def pydantic_schema_rate_limit(base_credentials: BaseCredentialsSchema):
    return {"successful": True}
