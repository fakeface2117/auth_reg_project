from datetime import datetime
from uuid import UUID

from pydantic import Field, BaseModel, ConfigDict


class OrderResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )

    id: int
    order_date: datetime
    order_status: str
    total_price: int = Field(gt=0)

class OneOrderResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )

    id: int
    order_id: int
    product_id: int
    product_count: int
    product_size: str
    name: str
    brand: str
    price: int

class UpdatedOrderResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )
    id: int
    user_id: UUID
    order_date: datetime
    order_status: str
    total_price: int = Field(gt=0)

class FilteredOrderResponse(UpdatedOrderResponse):
    pass

