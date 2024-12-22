from typing import List, Dict

from fastapi import APIRouter
from fastapi.params import Depends

from app.api.exceptions.base_http_exception import base_error_responses
from app.api.v1.products.rest_models import (AddProductRequest, NameBrandPrice, GetAllProductInfo, GetProductResponse,
                                             ProductsFilters, UpdatedProductData)
from app.services.products_service import ProductsService, get_products_service
from app.authorization.fastapi_users_auth.auth import current_user
from app.db.models import User
from app.decorators.admin_decorator import admin_verified

products_router = APIRouter(responses=base_error_responses)

products_tags: str = "Products"


@products_router.post(path='/addProduct', summary="Добавление админом одного товара")
@admin_verified  # проверка админа
async def add_new_product(
        product_data: AddProductRequest,
        user: User = Depends(current_user),  # получение текущего пользователя
        products_service: ProductsService = Depends(get_products_service)
) -> int:
    """Добавление админом одного товара"""
    new_product_id = await products_service.add_product(product_data=product_data.model_dump())
    return new_product_id


@products_router.post(path='/addManyProducts')
@admin_verified
async def add_products(
        products_data: List[AddProductRequest],
        user: User = Depends(current_user),
        products_service: ProductsService = Depends(get_products_service)
) -> List[Dict[str, int]]:
    """Добавление админом нескольких товаров одновременно"""
    # exclude_unset гарантирует что в словарь попадут явно заданные поля
    new_product_id = await products_service.add_many_products(
        products_data=[product_data.model_dump(exclude_unset=True) for product_data in products_data])
    return new_product_id


@products_router.get(path='/getAllProducts')
@admin_verified
async def get_all(
        user: User = Depends(current_user),
        products_service: ProductsService = Depends(get_products_service)
) -> List[GetAllProductInfo]:
    """Получение списка всех товаров (только для админа)"""
    all_products = await products_service.get_all_products()
    return all_products


@products_router.get(path='/getAllBrieflyProducts')
async def get_all_briefly(
        products_service: ProductsService = Depends(get_products_service)
) -> List[NameBrandPrice]:
    """Получение списка всех товаров в кратком представлении если они есть в наличии (для всех пользователей)"""
    briefly_all_products = await products_service.get_all_products_briefly()
    return briefly_all_products


@products_router.get(path='/getProductInfo')
async def get_product_info(
        product_id: int,
        products_service: ProductsService = Depends(get_products_service)
) -> GetProductResponse:
    """Получение подробной информации о товаре по id (для всех пользователей)"""
    product_info = await products_service.get_one_product(product_id=product_id)
    return product_info


@products_router.post(path='/getProductsByFilter')
async def get_products_by_filter(
        filter_info: ProductsFilters,
        products_service: ProductsService = Depends(get_products_service)
) -> List[NameBrandPrice]:
    """Получение информации о товарах по фильтрам (для всех пользователей)"""
    briefly_filtered_products = await products_service.get_by_filters(filter_data=filter_info)
    return briefly_filtered_products


@products_router.patch(path='/updateProductById')
@admin_verified
async def update_by_id(
        product_id: int,
        updated_data: UpdatedProductData,
        user: User = Depends(current_user),
        products_service: ProductsService = Depends(get_products_service)
) -> GetAllProductInfo:
    """Обновление товара по id товара (только админ)"""
    updated_product = await products_service.update_product_by_id(
        product_id=product_id, updated_data=updated_data.model_dump(exclude_none=True)
    )
    return updated_product


@products_router.delete(path='/deleteProductById')
@admin_verified
async def delete_by_id(
        product_id: int,
        user: User = Depends(current_user),
        products_service: ProductsService = Depends(get_products_service)
) -> str:
    """Удаление товара по id товара (только админ)"""
    result = await products_service.delete_product_by_id(product_id=product_id)
    return result
