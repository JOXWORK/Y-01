from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy.generics import now_utc
from sqlalchemy import select

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

from core.models.refresh_token import RefreshToken


class SQLAlchemyRefreshTokenDatabase:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, refresh_token_dict: dict[str, int, int]) -> RefreshToken:
        refresh_token = RefreshToken(**refresh_token_dict)
        self.session.add(refresh_token)
        await self.session.commit()
        await self.session.refresh(refresh_token)

        return refresh_token

    async def get_by_fingerprint(self, fingerprint: str) -> RefreshToken | None:
        query = select(RefreshToken).where(RefreshToken.fingerprint == fingerprint)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def revoke(self, refresh_token: RefreshToken) -> None:
        refresh_token.revoked_at = now_utc()
        await self.session.commit()
