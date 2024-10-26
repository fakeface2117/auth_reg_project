from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from loguru import logger

from api.metadata.tags_metadata import tags_metadata
from app.api.store_bucket.router_bucket import bucket_router
from app.authorization.fastapi_users_auth.auth import fastapi_users, auth_backend, current_user
from app.authorization.fastapi_users_auth.rest_models import UserRead, UserCreate, UserUpdate
from app.core.app_description import description
from app.core.config import settings
from app.db import pg_session
from app.db.models import User


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        pg_engine = create_async_engine(
            url=settings.DB_CONNECTION_STRING,
            future=True,
            echo=False
        )
        logger.info("Success create sqlalchemy engine.")

        pg_session.SessionLocal = async_sessionmaker(
            bind=pg_engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False
        )
        logger.info(f'Swagger: http://{settings.SERVICE_HOST}:{settings.SERVICE_PORT}/api/store/openapi')
        yield
    finally:
        logger.info("App stopp ...")


app = FastAPI(
    summary="Каой нибудь заголовок документации",
    docs_url='/api/store/openapi',
    openapi_url='/api/store/openapi.json',
    lifespan=lifespan
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="STORE API",
        version="1.0.0",
        description=description,
        routes=app.routes,
        tags=tags_metadata
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/store/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/store/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/api/store/auth",
    tags=["Auth"],
)


@app.get("/api/store/protected", tags=["Test protect"])
def protect_route(user: User = Depends(current_user)):
    return f"Hello {user.email}"


app.include_router(bucket_router, prefix='/api/store/v1/buckets')
# app.include_router(users_router, prefix='/api/store/v1/users')


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
    )
