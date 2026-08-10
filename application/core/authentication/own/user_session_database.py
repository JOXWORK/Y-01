from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy.generics import now_utc

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from core.models.user import User


from core.models.user_session import UserSession


class SQLAlchemyUserSessionDatabase:
    def __init__(
        self,
        session: AsyncSession,
        lifetime_seconds: float = 0,
        lifetime_minutes: float = 0,
        lifetime_hours: float = 0,
        lifetime_days: float = 0,
        lifetime_weeks: float = 0,
    ):
        self.session = session
        self.lifetime_seconds = lifetime_seconds
        self.lifetime_minutes = lifetime_minutes
        self.lifetime_hours = lifetime_hours
        self.lifetime_days = lifetime_days
        self.lifetime_weeks = lifetime_weeks

    async def create(self, user: User) -> UserSession:
        user_session = UserSession(user_id=user.id)
        self.session.add(user_session)
        await self.session.commit()
        await self.session.refresh(user_session)

        return user_session

    async def get(self, user_session_id: int) -> UserSession | None:
        return await self.session.get(UserSession, user_session_id)

    async def reissue_count_tick(self, user_session: UserSession) -> None:
        user_session.reissue_count += 1
        await self.session.commit()

    async def revoke(self, user_session: UserSession, force_revoke: bool = False) -> None:
        if not user_session.revoked_at or force_revoke:
            user_session.revoked_at = now_utc()
            await self.session.commit()

    async def destroy(self, user_session: UserSession) -> None:
        await self.session.delete(user_session)
        await self.session.commit()
