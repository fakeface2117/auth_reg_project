from datetime import datetime
from typing import Optional, Literal, List
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class AddBucketRequest(BaseModel):
    product_id: int = Field(gt=0)
    product_count: int = Field(gt=0)
    product_size: Literal['XS', 'S', 'M', 'L', 'XL', 'XXL']

class GetBucketResponse(BaseModel):
    # для работы с базой
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )

    id: int
    user_id: UUID
    added_at: Optional[datetime]
    product_count: int
    product_size: Literal['XS', 'S', 'M', 'L', 'XL', 'XXL']
    product_id: int
    name: str
    brand: str
    price: int

class GetBucketAll(BaseModel):
    total_price: int = Field(gt=0)
    products: List[GetBucketResponse]