from pydantic import BaseModel, Field


class AddProductRequest(BaseModel):
    name: str = Field(max_length=50)
    brand: str = Field(max_length=50)
    price: int = Field(gt=0)
    counts: int = Field(gt=0)
    description: str = Field(max_length=1000)

