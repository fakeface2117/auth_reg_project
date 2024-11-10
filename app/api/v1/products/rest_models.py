from pydantic import BaseModel


class AddProductResponse(BaseModel):
    name: str
    brand: str
    price: int
    counts: int
    description: str