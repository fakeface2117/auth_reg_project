from fastapi import APIRouter, Depends

from app.api.exceptions.base_http_exception import base_error_responses
from app.api.v1.orders.rest_models import UpdatedOrderResponse
from app.authorization.fastapi_users_auth.auth import current_user
from app.db.models import User
from app.db.sql_enums import OrderStatusEnum
from app.services.orders_sevice import get_order_service, OrderService
from app.services.payment_service import get_payment_service, PaymentService

payment_router = APIRouter(responses=base_error_responses)


@payment_router.post("/{order_id}")
async def buy_order(
        order_id: int,
        user: User = Depends(current_user),
        payment_service: PaymentService = Depends(get_payment_service),
        order_service: OrderService = Depends(get_order_service)
) -> UpdatedOrderResponse:
    """Оплата заказа"""
    payment_result = await payment_service.buy_new_order(user_id=user.id, order_id=order_id)
    if payment_result:
        result = await order_service.update_status(order_id=order_id, new_status=OrderStatusEnum.IS_PAID)
        return result  # TODO при окончательном подключении кошелька, надо использовать redirect на кошелек
    # TODO при наличии редиректа, разбить роутер на два (второй для вызова callback)
