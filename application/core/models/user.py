from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models.mixins import BaseIntIdPkMixin
from core.types_own.user_id import UserIdType

from .base import Base

if TYPE_CHECKING:
    pass


class User(
    Base,
    SQLAlchemyBaseUserTable[UserIdType],
    BaseIntIdPkMixin,
):
    name: Mapped[str | None] = mapped_column(String(50))
