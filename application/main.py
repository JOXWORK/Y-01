from contextlib import asynccontextmanager

import uvicorn
from api import router as api_router
from core.config import settings
from core.models import db_attach
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_attach.dispose()


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)
app.include_router(router=api_router)


def func_main():
    uvicorn.run(
        app=settings.host.uvc_app_path,
        host=settings.host.host,
        port=settings.host.port,
        reload=settings.host.uvc_reload,
        workers=settings.host.uvc_workers,
    )


if __name__ == "__main__":
    func_main()
