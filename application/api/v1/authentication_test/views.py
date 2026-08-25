from __future__ import annotations

from typing import TYPE_CHECKING

from core.authentication.rate_limiter import rate_limiter
from fastapi import APIRouter, Depends

from api.dependencies.auth import fastapi_current_user

if TYPE_CHECKING:
    from core.models.user import User

from .responses import IsUserValidResponse, SuccessfulResponse
from .schemas import BaseCredentialsSchema

router = APIRouter()


@router.get("/is-user-valid")
async def is_user_valid(user: User = Depends(fastapi_current_user)) -> IsUserValidResponse:
    return {"is_valid": True}


@router.post("/rate-limit")
@rate_limiter.restrain(
    kwarg_schema="user.id",
    endpoint_cfg=rate_limiter.config.rate_limit,
)
async def rate_limit(user: User = Depends(fastapi_current_user)) -> SuccessfulResponse:
    return {"successful": True}


@router.post("/user-email-rate-limit")
@rate_limiter.restrain(
    kwarg_schema="user.email",
    endpoint_cfg=rate_limiter.config.user_email_rate_limit,
)
async def user_email_rate_limit(user: User = Depends(fastapi_current_user)) -> SuccessfulResponse:
    return {"successful": True}


@router.post("/pydantic-schema-rate-limit")
@rate_limiter.restrain(
    kwarg_schema="base_credentials.email",
    endpoint_cfg=rate_limiter.config.pydantic_schema_rate_limit,
)
async def pydantic_schema_rate_limit(base_credentials: BaseCredentialsSchema) -> SuccessfulResponse:
    return {"successful": True}
