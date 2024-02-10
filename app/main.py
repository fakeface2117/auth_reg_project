import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.metadata.tags_metadata import tags_metadata

app = FastAPI(
    docs_url='/api/auth/openapi',
    openapi_url='/api/auth/openapi.json'
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="AUTH API",
        version="1.0.0",
        description="Auth project",
        routes=app.routes,
        tags=tags_metadata
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/api/auth/v1/test")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8090,
        # reload=True
    )
