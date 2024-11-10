from fastapi import APIRouter
from fastapi.params import Depends

from app.api.v1.products.rest_models import AddProductResponse
from app.services.products_service import ProductsService, get_products_service

products_router = APIRouter()

products_tags: str = "products"

@products_router.post(path='/addProduct', tags=[products_tags])
async def add_new_product(
        product_data: AddProductResponse,
        products_service: ProductsService = Depends(get_products_service)
):
    new_product_id = await products_service.add_product(product_data=product_data.dict())
    return new_product_id
