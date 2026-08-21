from __future__ import annotations

from typing import TYPE_CHECKING

from core.authentication.rate_limit_guard import rate_limit_guard
from fastapi import APIRouter, Depends

from api.dependencies.auth import fastapi_current_user

if TYPE_CHECKING:
    from core.models.user import User

router = APIRouter()


@router.get("/is-user-valid")
async def is_user_valid(user: User = Depends(fastapi_current_user)):
    return {"is_valid": True}


@router.post("/rate-limit")
@rate_limit_guard.keep_rate_limit()
async def rate_limit_endpoint(user: User = Depends(fastapi_current_user)):
    return {"message": "succsessful"}
