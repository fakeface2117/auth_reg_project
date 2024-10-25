import uvicorn
from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from loguru import logger

from api.metadata.tags_metadata import tags_metadata
from app.authorization.auth import fastapi_users, auth_backend, current_user
from app.authorization.rest_models import UserRead, UserCreate
# from app.authorization.auth import fastapi_users, auth_backend, current_user
from app.core.config import settings
# from app.authorization.rest_models import UserRead, UserCreate
# from app.core.config import CONNECTION_STRING
from app.db import pg_session
from app.db.models import User

app = FastAPI(
    docs_url='/api/store/openapi',
    openapi_url='/api/store/openapi.json',
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="STORE api",
        version="1.0.0",
        description="Store project",
        routes=app.routes,
        tags=tags_metadata
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.on_event('startup')
async def startup():
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


@app.on_event('shutdown')
async def shutdown():
    pass

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/store/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/store/auth",
    tags=["Auth"],
)


@app.get("/api/store/protected")
def protect_route(user: User = Depends(current_user)):
    return f"Hello {user.email}"


# app.include_router(users_router, prefix='/api/store/v1/users')


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8081,
        # reload=True
    )
