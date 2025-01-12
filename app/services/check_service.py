from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Products, StoreOrders
from app.db.pg_session import db_connection
from app.db.sql_enums import OrderStatusEnum


class CheckService:
    """Проверка наличия товара"""

    @db_connection
    async def check_product(self, session: AsyncSession, product_id: int, product_size: str, product_count: int,
                            return_result: bool = False):
        exists_criteria = select(
            Products.id,
            Products.name,
            Products.brand,
            Products.counts,
            Products.sum_count,
            Products.price
        ).filter_by(id=product_id)
        try:
            check = await session.execute(exists_criteria)
        except SQLAlchemyError as e:
            raise e
        product_data = check.fetchone()
        if not product_data:
            raise HTTPException(status_code=404, detail="Товара не существует")
        count_of_size = list(filter(lambda x: x['size'] == product_size, product_data.counts))
        if not count_of_size:
            raise HTTPException(
                status_code=404,
                detail=f"Размера {product_size} нет в наличии для выбранного товара '{product_data.name} {product_data.brand}'"
            )
        if count_of_size[0]['count'] < product_count:
            raise HTTPException(
                status_code=404,
                detail=f"В наличии только {count_of_size[0]['count']} шт. для выбранного товара '{product_data.name} {product_data.brand}'"
            )

        if return_result:
            return {
                "id": product_data.id,
                "sum_count": product_data.sum_count,
                "counts": product_data.counts
            }, product_data.price * product_count

    @db_connection
    async def check_order(self, session: AsyncSession, order_id: int, user_id: UUID):
        check_query = select(StoreOrders).filter(
            StoreOrders.id == order_id,
            StoreOrders.user_id == user_id,
            StoreOrders.order_status == OrderStatusEnum.CREATED
        )
        try:
            check = await session.execute(check_query)
        except SQLAlchemyError as e:
            raise e
        order_data = check.scalar_one_or_none()
        if not order_data:
            raise HTTPException(status_code=404, detail='Заказа не существует')
        return {'order_id': order_data.id, 'total_price': order_data.total_price}
