from fastapi import FastAPI
from contextlib import asynccontextmanager
from auth.routes import router as auth_router
from db.db import init_db,engine

API_PREFIX = "/api"
API_VERSION = "v1"



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

    engine.dispose()

app = FastAPI(lifespan= lifespan)

app.include_router(auth_router, prefix= f"{API_PREFIX}/{API_VERSION}")