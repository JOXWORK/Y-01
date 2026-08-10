from __future__ import annotations

from typing import TYPE_CHECKING

from core.authentication.own import SQLAlchemyRefreshTokenDatabase
from core.models import db_attach
from fastapi import Depends

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_refresh_token_db(session: AsyncSession = Depends(db_attach.new_session)):
    yield SQLAlchemyRefreshTokenDatabase(session=session)
