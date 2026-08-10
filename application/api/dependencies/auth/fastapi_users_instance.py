from core.models.user import User
from core.types_own.user_id import UserIdType
from fastapi_users import FastAPIUsers

from .backend import auth_backend
from .get_user_manager import get_user_manager

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
)

fastapi_current_user = fastapi_users.current_user(
    active=True,
    verified=False,
)

fastapi_current_superuser = fastapi_users.current_user(
    active=True,
    verified=True,
    superuser=True,
)
