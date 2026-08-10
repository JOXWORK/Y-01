# ruff: noqa: F401, I001

from core.config import settings
from fastapi import APIRouter

from .authentication.authentication import router as authentication_router
from .authentication.reissue import router as reissue_router
from .hello_world.views import router as hello_world_router

router = APIRouter(prefix=settings.api.v1.prefix.router_v1)


router.include_router(
    router=hello_world_router,
    tags=settings.api.v1.tags.hello_world,
    prefix=settings.api.v1.prefix.hello_world,
)

router.include_router(
    router=authentication_router,
    tags=settings.api.v1.tags.auth,
)

router.include_router(
    router=reissue_router,
    tags=settings.api.v1.tags.auth,
    prefix=settings.api.v1.prefix.auth,
)
