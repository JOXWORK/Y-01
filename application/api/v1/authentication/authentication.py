from core.config import settings
from core.schemas.authentication import UserCreate, UserRead, UserUpdate
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from api.dependencies.auth.backend import auth_backend
from api.dependencies.auth.fastapi_users_instance import fastapi_users

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.prefix.auth,
    dependencies=[Depends(http_bearer)],
)

router.include_router(
    fastapi_users.get_auth_router(backend=auth_backend),
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
)

router.include_router(
    fastapi_users.get_reset_password_router(),
)
