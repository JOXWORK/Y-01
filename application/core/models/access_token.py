from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy.access_token import (
    Mapped,
    SQLAlchemyBaseAccessTokenTable,
    String,
    mapped_column,
)
from sqlalchemy import ForeignKey

from core.types_own.user_id import UserIdType

from .base import Base

if TYPE_CHECKING:
    pass


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[UserIdType]):
    token: Mapped[str] = mapped_column(
        String(length=43),
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="users.id",
            ondelete="cascade",
        )
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="user_sessions.id",
            ondelete="cascade",
        )
    )
