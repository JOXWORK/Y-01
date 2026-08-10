# ruff: noqa: F401, I001

from core.config import settings
from fastapi import APIRouter

from .v1 import router as v1_router

router = APIRouter(prefix=settings.api.main_router.prefix)
router.include_router(router=v1_router)
