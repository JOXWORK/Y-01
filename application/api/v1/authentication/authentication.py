from core.config import settings
from core.schemas.authentication import UserCreate, UserRead, UserUpdate
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from api.dependencies.auth.backend import auth_backend
from api.dependencies.auth.fastapi_users_instance import fastapi_users
from api.dependencies.auth.routers.reset_own import get_reset_password_router
from api.dependencies.auth.routers.verify_own import get_verify_router

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.prefix.auth,
    dependencies=[Depends(http_bearer)],
)

router.include_router(
    fastapi_users.get_auth_router(backend=auth_backend),
)

router.include_router(
    fastapi_users.get_register_router(user_schema=UserRead, user_create_schema=UserCreate),
)

router.include_router(
    fastapi_users.get_users_router(user_schema=UserRead, user_update_schema=UserUpdate),
)

router.include_router(
    get_verify_router(user_schema=UserRead, get_user_manager=fastapi_users.get_user_manager),
)

router.include_router(
    get_reset_password_router(get_user_manager=fastapi_users.get_user_manager),
)
