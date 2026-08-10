from __future__ import annotations

from typing import TYPE_CHECKING

from core.authentication.own import SQLAlchemyAccessTokenDatabaseOwn
from core.models import db_attach
from core.models.access_token import AccessToken
from fastapi import Depends

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: AsyncSession = Depends(db_attach.new_session),
):
    yield SQLAlchemyAccessTokenDatabaseOwn(
        session=session,
        access_token_table=AccessToken,
    )
