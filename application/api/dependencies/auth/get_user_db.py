from __future__ import annotations

from typing import TYPE_CHECKING

from core.models import db_attach
from core.models.user import User
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(session: AsyncSession = Depends(db_attach.new_session)):
    yield SQLAlchemyUserDatabase(
        session=session,
        user_table=User,
    )
