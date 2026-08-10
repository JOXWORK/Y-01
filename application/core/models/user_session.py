from datetime import datetime

from fastapi_users_db_sqlalchemy.generics import now_utc
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import BaseIntIdPkMixin, UserSessionExpiresAtMixin


class UserSession(
    Base,
    BaseIntIdPkMixin,
    UserSessionExpiresAtMixin,
):
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

    reissue_count: Mapped[int] = mapped_column(server_default="0")
