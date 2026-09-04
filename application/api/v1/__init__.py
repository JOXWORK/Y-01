# ruff: noqa: F401, I001

from core.config import settings
from fastapi import APIRouter

from .authentication.authentication import router as authentication_router
from .authentication.reissue import router as reissue_router
from .hello_world.views import router as hello_world_router
from .authentication_test.views import router as authentication_test_router
from .rules.views import router as rules_router
from .message_moderation.views import router as message_moderation_router
from .task_response.views import router as task_response_router

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


router.include_router(
    router=authentication_test_router,
    tags=settings.api.v1.tags.auth_test,
    prefix=settings.api.v1.prefix.auth_test,
)

router.include_router(
    router=rules_router,
    tags=settings.api.v1.tags.rules,
    prefix=settings.api.v1.prefix.rules,
)

router.include_router(
    router=message_moderation_router,
    tags=settings.api.v1.tags.message_moderation,
    prefix=settings.api.v1.prefix.message_moderation,
)

router.include_router(
    router=task_response_router,
    tags=settings.api.v1.tags.task_response,
    prefix=settings.api.v1.prefix.task_response,
)
