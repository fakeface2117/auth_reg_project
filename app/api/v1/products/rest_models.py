from typing import Literal, Optional

from pydantic import BaseModel, Field


class ProductParameters(BaseModel):
    color: Literal['red', 'blue', 'white']
    style: Literal['sport', 'daily', 'home', 'office']
    season: Literal['winter', 'summer', 'demi_season']


class AddProductRequest(BaseModel):
    name: str = Field(max_length=50)
    brand: str = Field(max_length=50)
    price: int = Field(gt=0)
    counts: int = Field(gt=0)
    description: str = Field(max_length=1000)
    parameters: Optional[ProductParameters] = None
