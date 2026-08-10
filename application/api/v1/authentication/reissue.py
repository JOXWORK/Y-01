from __future__ import annotations

from typing import TYPE_CHECKING

from core.http.error_details import ReissueErrorDetails
from core.schemas.authentication import TokenRefreshSchema
from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies.auth import auth_backend, get_database_strategy

if TYPE_CHECKING:
    from core.authentication.own import StrategyOwn

router = APIRouter()


@router.post("/reissue")
async def reissue(
    token_schema: TokenRefreshSchema,
    strategy: StrategyOwn = Depends(get_database_strategy),
):
    response = await auth_backend.reissue(
        token=token_schema.refresh_token,
        strategy=strategy,
    )

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ReissueErrorDetails.BAD_REFRESH_TOKEN,
        )

    return response
