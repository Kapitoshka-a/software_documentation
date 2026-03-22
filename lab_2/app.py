from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings.create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
