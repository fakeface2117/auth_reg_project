from uuid import UUID

from app.services.check_service import CheckService


class PaymentService(CheckService):
    """Сервис оплаты заказов"""

    async def buy_new_order(self, user_id: UUID, order_id: int):
        """Оплата заказов"""

        # проверка заказа перед оплатой
        order_data = await self.check_order(order_id=order_id, user_id=user_id)

        """Код оплаты товара (например через YouMoney)"""

        return True


def get_payment_service():
    return PaymentService()
