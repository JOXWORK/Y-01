from __future__ import annotations

from typing import TYPE_CHECKING

from core.authentication.own import StrategyOwn
from core.config import settings
from fastapi import Depends

from .get_access_token_db import get_access_token_db
from .get_refresh_token_db import get_refresh_token_db
from .get_user_db import get_user_db
from .get_user_session_db import get_user_session_db

if TYPE_CHECKING:
    from core.authentication.own import (
        SQLAlchemyAccessTokenDatabaseOwn,
        SQLAlchemyRefreshTokenDatabase,
        SQLAlchemyUserSessionDatabase,
    )
    from fastapi_users.db import SQLAlchemyUserDatabase


async def get_database_strategy(
    user_database: SQLAlchemyUserDatabase = Depends(get_user_db),
    user_session_database: SQLAlchemyUserSessionDatabase = Depends(get_user_session_db),
    access_token_db: SQLAlchemyAccessTokenDatabaseOwn = Depends(get_access_token_db),
    refresh_token_db: SQLAlchemyRefreshTokenDatabase = Depends(get_refresh_token_db),
) -> StrategyOwn:
    return StrategyOwn(
        user_database=user_database,
        user_session_database=user_session_database,
        database=access_token_db,
        refresh_token_database=refresh_token_db,
        lifetime_seconds=settings.auth.access_token.lifetime_seconds,
    )
