from sqlalchemy.orm import Mapped, mapped_column

from core.models.mixins import BaseIntIdPkMixin

from .base import Base


class Example(Base, BaseIntIdPkMixin):
    example: Mapped[str] = mapped_column(
        default="example",
        server_default="example",
    )
