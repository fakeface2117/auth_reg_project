from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.store_bucket.rest_models import GetBucketResponse, AddBucketRequest, GetBucketAll
from app.db.models import StoreBucket, Products
from app.db.pg_session import db_connection
from app.services.check_service import CheckService


class BucketService(CheckService):
    """Сервис работы с корзиной"""

    @db_connection
    async def add_product_to_bucket(self, session: AsyncSession, user_id: UUID, product_info: AddBucketRequest) -> str:
        """Добавить товар в корзину"""

        await self.check_product(
            product_id=product_info.product_id,
            product_size=product_info.product_size,
            product_count=product_info.product_count
        )

        new_item = StoreBucket(
            user_id=user_id,
            product_id=product_info.product_id,
            product_count=product_info.product_count,
            product_size=product_info.product_size
        )
        session.add(new_item)
        try:
            await session.commit()  # flush если промежуточная фиксация данных
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return "Товар добавлен в корзину!"

    @db_connection
    async def get_bucket(self, session: AsyncSession, user_id: UUID) -> GetBucketAll:
        """Просмотр всей корзины"""
        query = select(
            StoreBucket.id,
            StoreBucket.user_id,
            StoreBucket.added_at,
            StoreBucket.product_count,
            StoreBucket.product_size,
            Products.id.label('product_id'),
            Products.name,
            Products.brand,
            Products.price
        )
        query = query.join(Products, Products.id == StoreBucket.product_id)
        query = query.where(StoreBucket.user_id == user_id).order_by(StoreBucket.added_at)
        try:
            result = await session.execute(query)
        except SQLAlchemyError as e:
            raise e
        records = result.all()
        if not records:
            raise HTTPException(status_code=404, detail="Ваша корзина пуста")
        total_price = sum(record.price * record.product_count for record in records)
        return GetBucketAll(
            total_price=total_price,
            products=[GetBucketResponse.model_validate(record) for record in records]
        )

    @db_connection
    async def delete_product_from_bucket(
            self,
            session: AsyncSession,
            user_id: UUID,
            product_id: int,
            product_size: str
    ) -> str:
        try:
            await session.execute(
                delete(StoreBucket).where(
                    StoreBucket.user_id == user_id,
                    StoreBucket.product_id == product_id,
                    StoreBucket.product_size == product_size
                )
            )
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return "Товар удален из корзины"


def get_bucket_service() -> BucketService:
    return BucketService()
