from typing import List, Literal

from fastapi import APIRouter, Depends

from app.api.exceptions.base_http_exception import base_error_responses
from app.api.v1.store_bucket.rest_models import AddBucketRequest, GetBucketResponse
from app.authorization.fastapi_users_auth.auth import current_user
from app.db.models import User
from app.services.bucket_service import BucketService, get_bucket_service

bucket_router = APIRouter(responses=base_error_responses)


@bucket_router.post("/postBucketOfUser")
async def post_user_bucket(
        product: AddBucketRequest,
        user: User = Depends(current_user),
        bucket_service: BucketService = Depends(get_bucket_service)
) -> str:
    """Добавление товара в корзину"""
    result = await bucket_service.add_product_to_bucket(product_info=product, user_id=user.id)
    return result


@bucket_router.get("/getBucketOfUser")
async def get_user_bucket(
        user: User = Depends(current_user),
        bucket_service: BucketService = Depends(get_bucket_service)
) -> List[GetBucketResponse]:
    """Просмотр корзины"""
    bucket = await bucket_service.get_bucket(user_id=user.id)
    return bucket


@bucket_router.delete("/deleteBucketOfUser",
                      description="Всегда удаляет все записи по заданным критериям, даже если записи нет. Сделано для избежания лишних проверок")
async def delete_item(
        product_id: int,
        product_size: Literal['XS', 'S', 'M', 'L', 'XL', 'XXL'],
        user: User = Depends(current_user),
        bucket_service: BucketService = Depends(get_bucket_service)
) -> str:
    """Удаление товара из корзины"""
    result = await bucket_service.delete_product_from_bucket(
        user_id=user.id,
        product_id=product_id,
        product_size=product_size
    )
    return result
