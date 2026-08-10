from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from sqlalchemy import select

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from core.models.access_token import AccessToken


class SQLAlchemyAccessTokenDatabaseOwn(
    SQLAlchemyAccessTokenDatabase,
):
    def __init__(self, session, access_token_table):
        super().__init__(session, access_token_table)

        self.session: AsyncSession
        self.access_token_table: AccessToken

    async def get_by_user_session_id(self, session_id: int) -> AccessToken | None:
        query = select(self.access_token_table).where(self.access_token_table.session_id == session_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
