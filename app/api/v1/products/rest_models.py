from pydantic import BaseModel, Field


class AddProductResponse(BaseModel):
    name: str = Field(max_length=50)
    brand: str = Field(max_length=50)
    price: int = Field(ge=0)
    counts: int = Field(ge=0)
    description: str = Field(max_length=1000)

