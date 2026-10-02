from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from app.config import settings

from app.database import init_db

from app.routes.api import router as api_router

from app.routes.web import router as web_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield


app = FastAPI(

    title=settings.app_name,

    description=(
        "AI fitness plan generator "
        "built with FastAPI and Gemini."
    ),

    version="1.0.0",

    lifespan=lifespan
)


app.mount(

    "/static",

    StaticFiles(
        directory="static"
    ),

    name="static"
)


app.include_router(
    web_router
)


app.include_router(
    api_router
)


@app.get(
    "/health",
    tags=["System"]
)
def health():

    return {

        "status": "ok",

        "service": settings.app_name
    }