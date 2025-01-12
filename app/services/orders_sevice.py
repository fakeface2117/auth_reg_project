from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.orders.rest_models import OrderResponse, OneOrderResponse, UpdatedOrderResponse, FilteredOrderResponse
from app.db.models import StoreBucket, Products, StoreOrders, StoreOrderProducts
from app.db.pg_session import db_connection
from app.db.sql_enums import OrderStatusEnum
from app.services.check_service import CheckService


class OrderService(CheckService):
    """Сервис заказов"""

    # TODO вынужденный ГОВНОКОД. Лучше завести отдельную таблицу для размеров
    @staticmethod
    def __unique_items(checked_items: list, items_in_bucket) -> list:
        """Функция для изменения данных размеров товаров.
        Если пользователь что-то купил, значит в таблице товаров надо вычесть"""
        unique_data = []
        seen_ids = set()
        for item in checked_items:
            if item['id'] not in seen_ids:
                unique_data.append(item)
                seen_ids.add(item['id'])

        for one_bucket_item in items_in_bucket:
            for one_checked_item in unique_data:
                if one_bucket_item.product_id == one_checked_item['id']:
                    def decrease_count(decrease_item):
                        if decrease_item['size'] == one_bucket_item.product_size:
                            decrease_item['count'] -= one_bucket_item.product_count
                        return decrease_item

                    one_checked_item['counts'] = list(map(decrease_count, one_checked_item['counts']))
                    one_checked_item['sum_count'] -= one_bucket_item.product_count

        return unique_data

    @db_connection
    async def add_order(self, session: AsyncSession, user_id: UUID) -> OrderResponse:
        """Создание заказа"""

        # получение данных корзины по user_id
        query = select(
            StoreBucket.id,
            StoreBucket.product_count,
            StoreBucket.product_size,
            StoreBucket.product_id
        ).where(StoreBucket.user_id == user_id)
        try:
            bucket_items = await session.execute(query)
        except SQLAlchemyError as e:
            raise e
        all_bucket_items = bucket_items.all()
        if not all_bucket_items:
            raise HTTPException(status_code=404, detail="Ваша корзина пуста")

        # проверка наличия товаров
        updated_products = []
        total_price = 0
        for one_product in all_bucket_items:
            updated_product, one_price = await self.check_product(
                product_id=one_product.product_id,
                product_size=one_product.product_size,
                product_count=one_product.product_count,
                return_result=True
            )
            updated_products.append(updated_product)
            total_price += one_price

        # подготовка данных для обновления таблицы товаров
        updated_products = self.__unique_items(updated_products, all_bucket_items)

        try:
            # создание заказа
            order_object = StoreOrders(
                user_id=user_id,
                order_status=OrderStatusEnum.CREATED,
                total_price=total_price
            )
            session.add(order_object)
            await session.flush()

            # создание записей о товарах в заказе
            order_products_object = [
                StoreOrderProducts(
                    order_id=order_object.id,
                    product_id=product_data.product_id,
                    product_count=product_data.product_count,
                    product_size=product_data.product_size
                ) for product_data in all_bucket_items
            ]
            session.add_all(order_products_object)
            await session.flush()

            # обновление таблицы товаров (декремент количества)
            await session.execute(update(Products), updated_products)
            await session.flush()

            # очистить корзину после заказа
            clear_user_bucket = delete(StoreBucket).where(StoreBucket.user_id == user_id)
            await session.execute(clear_user_bucket)
            await session.commit()

            return OrderResponse.model_validate(order_object)
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        except Exception as ex:
            await session.rollback()
            raise ex

    @db_connection
    async def get_user_orders(self, session: AsyncSession, user_id: UUID) -> list[OrderResponse]:
        """Получение всех заказов пользователя"""
        query = select(
            StoreOrders.id,
            StoreOrders.order_date,
            StoreOrders.order_status,
            StoreOrders.total_price
        ).where(StoreOrders.user_id == user_id)
        try:
            result = await session.execute(query)
        except SQLAlchemyError as e:
            raise e

        records = result.all()
        if not records:
            raise HTTPException(status_code=404, detail="Нет данных о заказах")
        return [OrderResponse.model_validate(record) for record in records]

    @db_connection
    async def get_user_order(self, session: AsyncSession, user_id: UUID, order_id: int) -> list[OneOrderResponse]:
        """Получение одного заказа пользователя"""

        query = select(
            StoreOrderProducts.id,
            StoreOrderProducts.order_id,
            StoreOrderProducts.product_id,
            StoreOrderProducts.product_count,
            StoreOrderProducts.product_size,
            Products.name,
            Products.brand,
            Products.price
        )
        query = query.join(Products, Products.id == StoreOrderProducts.product_id)
        query = query.join(StoreOrders, StoreOrders.id == StoreOrderProducts.order_id)
        query = query.where(StoreOrderProducts.order_id == order_id)
        query = query.where(StoreOrders.user_id == user_id)

        try:
            result = await session.execute(query)
        except SQLAlchemyError as e:
            raise e

        records = result.all()
        if not records:
            raise HTTPException(status_code=404, detail="Нет данных о заказе")
        return [OneOrderResponse.model_validate(record) for record in records]

    @db_connection
    async def get_filtered_order(self, session: AsyncSession, order_status: str) -> list[FilteredOrderResponse]:
        """Получение админом заказов по статусу"""
        query = select(StoreOrders).where(StoreOrders.order_status == order_status)
        try:
            result = await session.execute(query)
        except SQLAlchemyError as e:
            raise e
        records = result.scalars().all()
        if not records:
            raise HTTPException(status_code=404, detail="Нет данных о заказах с таким статусом")
        return [FilteredOrderResponse.model_validate(record) for record in records]

    @db_connection
    async def update_status(self, session: AsyncSession, order_id: int, new_status: str) -> UpdatedOrderResponse:
        """Обновление статуса заказа админом"""

        query = update(StoreOrders).filter_by(id=order_id).values(order_status=new_status).returning(StoreOrders)
        try:
            result = await session.execute(query)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        record = result.scalar_one_or_none()
        if not record:
            raise HTTPException(status_code=404, detail=f'Заказа с id={order_id} не существует')
        return UpdatedOrderResponse.model_validate(record)


def get_order_service() -> OrderService:
    return OrderService()
