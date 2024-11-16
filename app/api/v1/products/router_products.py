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
@admin_verified
async def add_new_product(
        product_data: AddProductRequest,
        user: User = Depends(current_user),
        products_service: ProductsService = Depends(get_products_service)
) -> int:
    new_product_id = await products_service.add_product(product_data=product_data.model_dump())
    return new_product_id


