from mixins import BaseIntIdPkMixin
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ModerationRule(Base, BaseIntIdPkMixin):
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="users.id",
            ondelete="cascade",
        )
    )

    rules: Mapped[dict[str, str]] = mapped_column(JSON, nullable=False)
