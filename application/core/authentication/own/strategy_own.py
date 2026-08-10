from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe
from typing import TYPE_CHECKING

from fastapi_users import exceptions
from fastapi_users.authentication.strategy.db import DatabaseStrategy

from core.authentication.validator import validator
from core.config import settings

from .exceptions_own import (
    RefreshTokenRevoked,
    UserSessionInvalid,
    UserSessionMaxReissueAmount,
)

if TYPE_CHECKING:
    from fastapi_users import BaseUserManager
    from fastapi_users.db import SQLAlchemyUserDatabase

    from core.models.access_token import AccessToken
    from core.models.refresh_token import RefreshToken
    from core.models.user import User
    from core.models.user_session import UserSession

    from .access_token_own import SQLAlchemyAccessTokenDatabaseOwn
    from .refresh_token_database import SQLAlchemyRefreshTokenDatabase
    from .user_session_database import SQLAlchemyUserSessionDatabase


class StrategyOwn(DatabaseStrategy):
    def __init__(
        self,
        user_database: SQLAlchemyUserDatabase,
        user_session_database: SQLAlchemyUserSessionDatabase,
        database: SQLAlchemyAccessTokenDatabaseOwn,
        refresh_token_database: SQLAlchemyRefreshTokenDatabase,
        lifetime_seconds=None,
    ):
        self.user_database = user_database
        self.user_session_database = user_session_database
        self.refresh_token_database = refresh_token_database
        super().__init__(database, lifetime_seconds)

        self.database: SQLAlchemyAccessTokenDatabaseOwn

    async def read_token(
        self,
        token: str | None,
        user_manager: BaseUserManager,
    ) -> User | None:
        if token is None:
            return None

        max_age = None
        if self.lifetime_seconds:
            max_age = datetime.now(timezone.utc) - timedelta(seconds=self.lifetime_seconds)

        access_token = await self.database.get_by_token(token, max_age)
        if access_token is None:
            return None

        user_session = await self.user_session_database.get(access_token.session_id)
        if user_session is None:
            return None

        try:
            await validator.check_user_session(user_session=user_session, force_raise=True)
            parsed_id = user_manager.parse_id(access_token.user_id)
            return await user_manager.get(parsed_id)
        except (exceptions.UserNotExists, exceptions.InvalidID, UserSessionInvalid):
            return None

    async def write_token(self, user: User) -> tuple[str, str] | None:
        user_session = await self.user_session_database.create(user=user)

        access_token, refresh_token_wrap = await self._create_token_pair(user=user, user_session=user_session)

        return access_token.token, refresh_token_wrap["token"]

    async def reissue_token(self, token: str) -> dict[str, str, str, str] | None:
        token_fingerprint = await self._hmac_digest(message=token)

        errors = []

        refresh_token = await self.refresh_token_database.get_by_fingerprint(token_fingerprint)
        if refresh_token is None:
            return None

        errors.extend(await validator.check_refresh_token(refresh_token=refresh_token) or [])

        user_session = await self.user_session_database.get(refresh_token.session_id)
        await self.user_session_database.reissue_count_tick(user_session)
        errors.extend(await validator.check_user_session(user_session=user_session) or [])

        user = await self.user_database.get(refresh_token.user_id)
        errors.extend(await validator.check_user(user=user) or [])

        if RefreshTokenRevoked in errors or exceptions.UserInactive in errors or UserSessionMaxReissueAmount in errors:
            await self.user_session_database.revoke(user_session)

        if errors:
            return None

        access_token = await self.database.get_by_user_session_id(user_session.id)
        if access_token is None:
            return None

        await self.database.delete(access_token)
        await self.refresh_token_database.revoke(refresh_token)

        access_token, refresh_token_wrap = await self._create_token_pair(user=user, user_session=user_session)

        return {
            "access_token": access_token.token,
            "refresh_token": refresh_token_wrap["token"],
        }

    async def destroy_token(self, token: str, user: User, *, session_destroy: bool = False) -> None:
        access_token = await self.database.get_by_token(token)
        if access_token is not None:
            user_session = await self.user_session_database.get(access_token.session_id)
            if user_session is not None:
                if not session_destroy:
                    await self.user_session_database.revoke(user_session)
                    await self.database.delete(access_token)
                else:
                    await self.user_session_database.destroy(user_session)

    def _create_access_token_dict(
        self,
        user: User,
        user_session_id: int,
    ) -> dict[str, int, int]:
        token = token_urlsafe()
        return {
            "token": token,
            "session_id": user_session_id,
            "user_id": user.id,
        }

    async def _create_refresh_token_dict(
        self,
        user: User,
        user_session_id: int,
    ) -> dict[str, str, int, int]:
        refresh_token = token_urlsafe()

        hmac_fingerprint = await self._hmac_digest(
            message=refresh_token,
        )

        return {
            "refresh_token": refresh_token,
            "fingerprint": hmac_fingerprint,
            "session_id": user_session_id,
            "user_id": user.id,
        }

    async def _create_token_pair(
        self, user: User, user_session: UserSession
    ) -> tuple[AccessToken, dict[str, str, str, RefreshToken]]:
        access_token_dict = self._create_access_token_dict(
            user=user,
            user_session_id=user_session.id,
        )

        refresh_token_dict = await self._create_refresh_token_dict(
            user=user,
            user_session_id=user_session.id,
        )
        raw_refresh_token = refresh_token_dict.pop("refresh_token")

        access_token = await self.database.create(access_token_dict)
        refresh_token = await self.refresh_token_database.create(refresh_token_dict)  # noqa: F841

        refresh_token_wrap = {"token": raw_refresh_token, "refresh_token": refresh_token}

        return access_token, refresh_token_wrap

    async def _hmac_digest(
        self,
        message: str,
        key: str = settings.auth.refresh_token.hmac_secret,
        digestmod=hashlib.sha256,
    ) -> str:
        hmac_ = hmac.new(
            key=key.encode(),
            msg=message.encode(),
            digestmod=digestmod,
        )

        return hmac_.hexdigest()
