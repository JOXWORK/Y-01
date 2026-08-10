# ruff: noqa: F401, I001

from .backend import auth_backend
from .fastapi_users_instance import fastapi_current_superuser, fastapi_current_user
from .get_database_strategy import get_database_strategy
from .get_user_db import get_user_db
from .get_user_manager import get_user_manager

__all__ = (
    "get_user_db",
    "get_user_manager",
    "fastapi_current_user",
    "fastapi_current_superuser",
    "get_token_catcher",
    "auth_backend",
    "get_database_strategy",
)
