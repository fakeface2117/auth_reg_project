from fastapi import APIRouter, Depends

from app.api.exceptions.base_http_exception import base_error_responses
from app.api.v1.orders.rest_models import CreateOrderResponse
from app.authorization.fastapi_users_auth.auth import current_user
from app.db.models import User
from app.services.orders_sevice import get_order_service, OrderService

order_router = APIRouter(responses=base_error_responses)


@order_router.post("/new")
async def create_order(
        user: User = Depends(current_user),
        order_service: OrderService = Depends(get_order_service)
) -> CreateOrderResponse:
    """Создание заказа"""
    result = await order_service.add_order(user_id=user.id)
    return result
