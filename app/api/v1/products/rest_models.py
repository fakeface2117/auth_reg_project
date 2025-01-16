from collections import defaultdict
from datetime import datetime
from typing import Literal, Optional, List, Any

from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator

from app.core.logger import logger


class BaseMappedModel(BaseModel):
    """Класс для реализации мапинга между моделями ORM и Pydantic"""
    # для работы с базой
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )


class BaseLowerCaseModel(BaseModel):
    @model_validator(mode='before')
    @classmethod
    def lower_name_brand(cls, data: Any):
        """Приведение к нижнему регистру полей name и brand"""
        if isinstance(data, dict):
            if data.get('name', None):
                data['name'] = data['name'].lower()
            if data.get('brand', None):
                data['brand'] = data['brand'].lower()
            return data


class ProductParameters(BaseModel):
    color: Literal['red', 'blue', 'white']
    style: Literal['sport', 'daily', 'home', 'office']
    season: Literal['winter', 'summer', 'demi_season']


class SizesCountsModel(BaseModel):
    size: Literal['XS', 'S', 'M', 'L', 'XL', 'XXL']
    count: int = Field(ge=0)


class AddProductRequest(BaseLowerCaseModel):
    name: str = Field(max_length=50)
    brand: str = Field(max_length=50)
    price: int = Field(gt=0, le=1000000000)
    sum_count: int = Field(ge=0)
    counts: List[SizesCountsModel]  # TODO лучше делать с доп таблицами для доп фильтрации и удобства
    description: str = Field(max_length=1000)
    parameters: Optional[ProductParameters] = None  # TODO лучше делать с доп таблицами для доп фильтрации и удобства

    @model_validator(mode='before')
    @classmethod
    def validate_sums(cls, data: Any):
        """Проверка соответствия общего количества товара и количества по размерам товаров"""
        if isinstance(data, dict):
            sum_count = data.get('sum_count', 0)
            counts = data.get('counts', [])
            sizes_data = sum(one_size.get('count', 0) for one_size in counts)
            if sum_count != sizes_data:
                logger.warning('Validation warning: incorrect sizes and counts')
                raise ValueError(f"Несоответствие данных по размерам ({sizes_data}) и общему количеству ({sum_count})")
            data['sum_count'] = sum_count
            return data

    @field_validator('counts')
    def correct_counts(cls, value: List[SizesCountsModel] | None):
        """Функция позволяет на этапе валидации объединить данные по нескольким размерам, если они повторяются"""
        if value:
            grouped_dict = defaultdict(int)
            for item in value:
                grouped_dict[item.size] += item.count
            return [SizesCountsModel(size=s, count=c) for s, c in grouped_dict.items()]


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
    id: int
    name: str = Field(max_length=50)
    brand: str = Field(max_length=50)
    price: int = Field(gt=0)
    counts: List[SizesCountsModel]
    description: str = Field(max_length=1000)
    parameters: Optional[ProductParameters] = None


class ProductsFilters(BaseLowerCaseModel):
    name: Optional[str] = Field(max_length=50, default=None)
    brand: Optional[str] = Field(max_length=50, default=None)
    price_min: int = Field(gt=0, default=1)
    price_max: int = Field(le=1000000000, default=1000000000)


class UpdatedProductData(BaseLowerCaseModel):
    name: str | None = Field(max_length=50, default=None)
    brand: str | None = Field(max_length=50, default=None)
    price: int | None = Field(gt=0, le=1000000000, default=None)
    sum_count: int | None = Field(ge=0, default=None)
    description: str | None = Field(max_length=1000, default=None)
    parameters: ProductParameters | None = None
    counts: List[SizesCountsModel] | None = None

    @model_validator(mode='before')
    @classmethod
    def validate_sums(cls, data: Any):
        """Валидация общего количества товаров и количества по размерам"""
        if isinstance(data, dict):
            sum_count = data.get('sum_count')
            counts = data.get('counts')
            if sum_count:
                if not counts:
                    logger.warning('Validation warning: update count of product')
                    raise ValueError('При обновлении общего количества необходимо также обновить данные по размерам')
            if counts:
                sizes_data = sum(one_size.get('count') for one_size in counts)
                if not sum_count:
                    sum_count = sizes_data
                    data['sum_count'] = sum_count
                if sum_count != sizes_data:
                    logger.warning('Validation error: incorrect sizes and counts')
                    raise ValueError(
                        f"Несоответствие данных по размерам ({sizes_data}) и общему количеству ({sum_count})")
            return data

    @field_validator('counts')
    def correct_counts(cls, value: List[SizesCountsModel] | None):
        """Функция позволяет на этапе валидации объединить данные по нескольким размерам, если они повторяются"""
        if value:
            grouped_dict = defaultdict(int)
            for item in value:
                grouped_dict[item.size] += item.count
            return [SizesCountsModel(size=s, count=c) for s, c in grouped_dict.items()]
