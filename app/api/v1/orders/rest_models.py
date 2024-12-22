from datetime import datetime

from pydantic import Field, BaseModel, ConfigDict


class CreateOrderResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )

    id: int
    order_date: datetime
    order_status: str
    total_price: int = Field(gt=0)
