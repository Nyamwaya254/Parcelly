from fastapi import FastAPI
from contextlib import asynccontextmanager
from auth.routes import router as auth_router
from db.db import init_db,engine
from scalar_fastapi import get_scalar_api_reference

API_PREFIX = "/api"
API_VERSION = "v1"



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

    engine.dispose()

app = FastAPI(lifespan= lifespan)

app.include_router(auth_router, prefix= f"{API_PREFIX}/{API_VERSION}")

#Scalar api Documentation    
@app.get("/scalar",include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )