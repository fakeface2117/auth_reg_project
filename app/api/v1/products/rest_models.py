from datetime import datetime
from typing import Literal, Optional, List, Any

from pydantic import BaseModel, Field, ConfigDict, root_validator, model_validator, validator, field_validator


class BaseMappedModel(BaseModel):
    """Класс для реализации мапинга между моделями ORM и Pydantic"""
    # для работы с базой
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )


class ProductParameters(BaseModel):
    color: Literal['red', 'blue', 'white']
    style: Literal['sport', 'daily', 'home', 'office']
    season: Literal['winter', 'summer', 'demi_season']


class SizesCountsModel(BaseModel):
    size: Literal['XS', 'S', 'M', 'L', 'XL', 'XXL']
    count: int = Field(ge=0)


class AddProductRequest(BaseModel):
    name: str = Field(max_length=50)
    brand: str = Field(max_length=50)
    price: int = Field(gt=0, le=1000000000)
    sum_count: int = Field(ge=0)
    counts: List[SizesCountsModel]  # TODO лучше делать с доп таблицами для доп фильтрации и удобства
    description: str = Field(max_length=1000)
    parameters: Optional[ProductParameters] = None  # TODO лучше делать с доп таблицами для доп фильтрации и удобства

    @model_validator(mode='before')
    @classmethod
    def validate_atts(cls, data: Any):
        if isinstance(data, dict):
            sum_count = data.get('sum_count')
            counts = data.get('counts')
            sizes_data = sum(one_size.get('count') for one_size in counts)
            if sum_count != sizes_data:
                raise ValueError(f"Несоответствие данных по размерам ({sizes_data}) и общему количеству ({sum_count})")
            return data


class GetAllProductInfo(BaseMappedModel):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    name: str
    brand: str
    price: int
    sum_count: int
    counts: List[SizesCountsModel]
    description: Optional[str] = None
    parameters: Optional[ProductParameters] = None


class NameBrandPrice(BaseMappedModel):
    id: int
    name: str = Field(max_length=50)
    brand: str = Field(max_length=50)
    price: int = Field(gt=0)


class GetProductResponse(BaseMappedModel):
    name: str = Field(max_length=50)
    brand: str = Field(max_length=50)
    price: int = Field(gt=0)
    counts: List[SizesCountsModel]
    description: str = Field(max_length=1000)
    parameters: Optional[ProductParameters] = None


class ProductsFilters(BaseModel):
    name: Optional[str] = Field(max_length=50, default=None)
    brand: Optional[str] = Field(max_length=50, default=None)
    price_min: int = Field(gt=0, default=1)
    price_max: int = Field(le=1000000000, default=1000000000)
