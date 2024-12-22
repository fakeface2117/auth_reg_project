from typing import List
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from app.api.v1.store_bucket.rest_models import GetBucketResponse, AddBucketRequest, GetBucketAll
from app.db.models import StoreBucket, Products
from app.db.pg_session import db_connection


class BucketService:
    """Сервис работы с корзиной"""

    @db_connection
    async def add_product_to_bucket(self, session: AsyncSession, user_id: UUID, product_info: AddBucketRequest) -> str:
        """Добавить товар в корзину"""

        exists_criteria = select(Products.id, Products.counts).filter_by(id=product_info.product_id)
        try:
            check = await session.execute(exists_criteria)
        except SQLAlchemyError as e:
            raise e
        product_data = check.fetchone()
        if not product_data:
            raise HTTPException(status_code=404, detail="Товара не существует")
        count_of_size = list(filter(lambda x: x['size'] == product_info.product_size, product_data.counts))
        if not count_of_size:
            raise HTTPException(status_code=404, detail=f"Размера {product_info.product_size} нет в наличии")
        if count_of_size[0]['count'] < product_info.product_count:
            raise HTTPException(status_code=404, detail=f"В наличии {count_of_size} шт.")

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
        query = query.join(Products, Products.id == StoreBucket.product_id).where(StoreBucket.user_id == user_id)
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
            raise e
        return "Товар удален из корзины"


def get_bucket_service() -> BucketService:
    return BucketService()
