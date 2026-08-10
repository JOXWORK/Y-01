from __future__ import annotations

from typing import TYPE_CHECKING

from core.authentication.own import SQLAlchemyUserSessionDatabase
from core.config import settings
from core.models import db_attach
from fastapi import Depends

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_session_db(session: AsyncSession = Depends(db_attach.new_session)):
    yield SQLAlchemyUserSessionDatabase(
        session=session,
        lifetime_minutes=settings.auth.user_session.lifetime_minutes,
        lifetime_hours=settings.auth.user_session.lifetime_hours,
        lifetime_days=settings.auth.user_session.lifetime_days,
    )
