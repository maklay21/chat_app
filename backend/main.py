from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.logging_config import _setup_logger
from config.settings import settings
from api.main import api_router


@asynccontextmanager
async def init_on_startup(app: FastAPI):
    _setup_logger()
    yield
    

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=init_on_startup,
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_STR)
