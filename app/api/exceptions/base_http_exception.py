from pydantic import BaseModel


class HTTPError(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }


base_error_responses = {
    404: {
        "model": HTTPError,
        "description": "Not found error",
    },
    500: {
        "model": HTTPError,
        "description": "Internal server error",
    }
}
