import contextlib
import pathlib

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from sdapp.logger import logger
from sdapp.routers.images import router as images_router
from sdapp.routers.users import router as users_router
from sdapp.settings import settings
from sdapp.storage import STATIC_ROOT


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.debug:
        settings_context = logger.bind(**settings.model_dump())
        settings_context.debug("Settings were loaded")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(images_router, prefix="/images", tags=["images"])

app.mount("/static", StaticFiles(directory=STATIC_ROOT), name="static")
