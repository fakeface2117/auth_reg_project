from fastapi import APIRouter, Depends

from app.api.exceptions.base_http_exception import base_error_responses
from app.api.v1.orders.rest_models import OrderResponse, OneOrderResponse, UpdatedOrderResponse, FilteredOrderResponse
from app.authorization.fastapi_users_auth.auth import current_user
from app.db.models import User
from app.db.sql_enums import OrderStatusEnum
from app.decorators.admin_decorator import admin_verified
from app.services.orders_sevice import get_order_service, OrderService

order_router = APIRouter(responses=base_error_responses)


@order_router.post("/add")
async def create_order(
        user: User = Depends(current_user),
        order_service: OrderService = Depends(get_order_service)
) -> OrderResponse:
    """Создание заказа"""
    result = await order_service.add_order(user_id=user.id)
    return result


@order_router.get("/user-orders")
async def get_orders(
        user: User = Depends(current_user),
        order_service: OrderService = Depends(get_order_service)
) -> list[OrderResponse]:
    """Получение всех заказов"""
    result = await order_service.get_user_orders(user_id=user.id)
    return result


@order_router.get("/user-orders/{order_id}")
async def get_order(
        order_id: int,
        user: User = Depends(current_user),
        order_service: OrderService = Depends(get_order_service)
) -> list[OneOrderResponse]:
    """Получение информации о заказе"""
    result = await order_service.get_user_order(user_id=user.id, order_id=order_id)
    return result


@order_router.get("/filer-orders")
@admin_verified
async def get_orders_by_status_filter(
        order_status: OrderStatusEnum,
        user: User = Depends(current_user),
        order_service: OrderService = Depends(get_order_service)
) -> list[FilteredOrderResponse]:
    """Получение списка заказов по статусам (только админ)"""
    result = await order_service.get_filtered_order(order_status=order_status)
    return result


@order_router.patch("/user-orders/{order_id}")
@admin_verified
async def update_order_status(
        order_id: int,
        new_status: OrderStatusEnum,
        user: User = Depends(current_user),
        order_service: OrderService = Depends(get_order_service)
) -> UpdatedOrderResponse:
    """Обновление статуса заказа (только админ)"""
    result = await order_service.update_status(order_id=order_id, new_status=new_status)
    return result
