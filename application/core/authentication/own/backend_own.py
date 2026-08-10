from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi_users.authentication import AuthenticationBackend

if TYPE_CHECKING:
    from fastapi import Response

    from core.models.user import User

    from .bearer_own import BearerTransportOwn
    from .strategy_own import StrategyOwn


class AuthenticationBackendOwn(AuthenticationBackend):
    def __init__(self, name, transport, get_strategy):
        super().__init__(name, transport, get_strategy)

        self.transport: BearerTransportOwn

    async def login(self, strategy: StrategyOwn, user: User) -> Response:
        access_token, refresh_token = await strategy.write_token(user)
        return await self.transport.get_login_response(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def reissue(
        self,
        token: str,
        strategy: StrategyOwn,
    ) -> Response:
        response_dict = await strategy.reissue_token(
            token=token,
        )

        if response_dict is None:
            return None

        return await self.transport.get_reissue_response(**response_dict)
