from typing import List, Dict

from fastapi import APIRouter
from fastapi.params import Depends

from app.api.v1.products.rest_models import AddProductRequest
from app.services.products_service import ProductsService, get_products_service
from app.authorization.fastapi_users_auth.auth import current_user
from app.db.models import User
from app.decorators.admin_decorator import admin_verified

products_router = APIRouter()

products_tags: str = "Products"


@products_router.post(path='/addProduct', tags=[products_tags])
@admin_verified # проверка админа
async def add_new_product(
        product_data: AddProductRequest,
        user: User = Depends(current_user), # получение текущего пользователя
        products_service: ProductsService = Depends(get_products_service)
) -> int:
    """Добавление админом одного товара"""
    new_product_id = await products_service.add_product(product_data=product_data.model_dump())
    return new_product_id


@products_router.post(path='/addManyProducts', tags=[products_tags])
@admin_verified
async def add_products(
        products_data: List[AddProductRequest],
        user: User = Depends(current_user),
        products_service: ProductsService = Depends(get_products_service)
) -> List[Dict[str, int]]:
    """Добавление админом нескольких товаров одновременно"""
    new_product_id = await products_service.add_many_products(
        products_data=[product_data.model_dump() for product_data in products_data])
    return new_product_id




