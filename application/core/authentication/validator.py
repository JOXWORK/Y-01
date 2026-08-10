from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy.generics import now_utc

if TYPE_CHECKING:
    from core.models.refresh_token import RefreshToken
    from core.models.user import User
    from core.models.user_session import UserSession

from fastapi_users.exceptions import UserInactive, UserNotExists

from core.config import settings

from .own.exceptions_own import (
    RefreshTokenNotExists,
    RefreshTokenRevoked,
    UserSessionExpires,
    UserSessionMaxReissueAmount,
    UserSessionNotExists,
    UserSessionRevoked,
)


class Validator:
    def __init__(
        self,
        force_raise: bool = False,
        lifetime_seconds: float = 0,
        lifetime_minutes: float = 0,
        lifetime_hours: float = 0,
        lifetime_days: float = 0,
        lifetime_weeks: float = 0,
        reissue_max_amount: int = 0,
    ):
        self.force_raise = force_raise
        self.lifetime_seconds = lifetime_seconds
        self.lifetime_minutes = lifetime_minutes
        self.lifetime_hours = lifetime_hours
        self.lifetime_days = lifetime_days
        self.lifetime_weeks = lifetime_weeks
        self.reissue_max_amount = reissue_max_amount

    async def check_user_session(
        self,
        user_session: UserSession,
        force_raise: bool = False,
        not_exists_raise: bool = False,
    ) -> list[UserSessionExpires | UserSessionRevoked | UserSessionNotExists] | None:
        force_raise_ = await self._force_raise_digest(force_raise=force_raise)
        errors = []

        if not_exists_raise and user_session is None:
            if force_raise_:
                raise UserSessionNotExists()
            errors.append(UserSessionNotExists)

        if user_session.reissue_count >= self.reissue_max_amount:
            if force_raise_:
                raise UserSessionMaxReissueAmount()
            errors.append(UserSessionMaxReissueAmount)

        if not hasattr(user_session, "expires_at"):
            user_session_expires_at = user_session.created_at + timedelta(
                seconds=self.lifetime_seconds,
                minutes=self.lifetime_minutes,
                hours=self.lifetime_hours,
                days=self.lifetime_days,
                weeks=self.lifetime_weeks,
            )
        else:
            user_session_expires_at = user_session.expires_at

        if now_utc() > user_session_expires_at:
            if force_raise_:
                raise UserSessionExpires()
            errors.append(UserSessionExpires)

        if user_session.revoked_at:
            if force_raise_:
                raise UserSessionRevoked()
            errors.append(UserSessionRevoked)

        if not errors:
            return None

        return errors

    async def check_refresh_token(
        self,
        refresh_token: RefreshToken,
        force_raise: bool | None = None,
        not_exists_raise: bool = False,
    ) -> list[RefreshTokenRevoked | RefreshTokenNotExists] | None:
        force_raise_ = await self._force_raise_digest(force_raise=force_raise)
        errors = []

        if not_exists_raise and refresh_token is None:
            if force_raise_:
                raise RefreshTokenNotExists()
            errors.append(RefreshTokenNotExists)

        if refresh_token.revoked_at:
            if force_raise_:
                raise RefreshTokenRevoked()
            errors.append(RefreshTokenRevoked)

        if not errors:
            return None

        return errors

    async def check_user(
        self,
        user: User,
        force_raise: bool | None = None,
        not_exists_raise: bool = False,
    ) -> list[UserInactive | UserNotExists] | None:
        force_raise_ = await self._force_raise_digest(force_raise=force_raise)
        errors = []

        if not_exists_raise and user is None:
            if force_raise_:
                raise UserNotExists()
            errors.append(UserNotExists)

        if not user.is_active:
            if force_raise_:
                raise UserInactive()
            errors.append(UserInactive)

        if not errors:
            return None

        return errors

    async def _force_raise_digest(self, force_raise: bool) -> bool:
        if self.force_raise and force_raise or force_raise:
            return True
        return force_raise


validator = Validator(
    force_raise=False,
    lifetime_minutes=settings.auth.user_session.lifetime_minutes,
    lifetime_hours=settings.auth.user_session.lifetime_hours,
    lifetime_days=settings.auth.user_session.lifetime_days,
    reissue_max_amount=settings.auth.user_session.reissue_max_amount,
)
