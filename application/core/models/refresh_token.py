from datetime import datetime

from fastapi_users_db_sqlalchemy.generics import now_utc
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import BaseIntIdPkMixin


class RefreshToken(Base, BaseIntIdPkMixin):
    fingerprint: Mapped[str] = mapped_column(String(1024))

    session_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="user_sessions.id",
            ondelete="cascade",
        )
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="users.id",
            ondelete="cascade",
        )
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
        default=now_utc,
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        index=True,
    )

    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        index=True,
    )
