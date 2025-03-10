from datetime import datetime

from fastapi import HTTPException
from typing import List, Dict, Any

from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.products.rest_models import NameBrandPrice, GetAllProductInfo, GetProductResponse, ProductsFilters
from app.core.logger import logger
from app.db.models import Products
from app.db.pg_session import db_connection


class ProductsService:
    """Сервис работы с товарами"""

    @db_connection
    async def add_product(self, session: AsyncSession, product_data: Dict) -> int:
        """Добавить товар"""
        new_product = Products(**product_data)
        session.add(new_product)
        try:
            await session.commit()  # flush если промежуточная фиксация данных
        except SQLAlchemyError as e:
            logger.error(f'Add product error: {e}')
            await session.rollback()
            raise e
        return new_product.id

    @db_connection
    async def add_many_products(self, session: AsyncSession, products_data: List[Dict[str, Any]]) -> List[Dict]:
        """Добавить несколько товаров"""
        new_products = [Products(**product_data) for product_data in products_data]
        session.add_all(new_products)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            logger.error(f'Add many products error: {e}')
            await session.rollback()
            raise e
        return [{"id_product": row.id} for row in new_products]

    @db_connection
    async def get_all_products(self, session: AsyncSession) -> List[GetAllProductInfo]:
        """Получение всей инфы обо всех товарах (для админа)"""
        query = select(Products)
        try:
            result = await session.execute(query)
        except SQLAlchemyError as e:
            logger.error(f'Get all products error: {e}')
            raise e
        # Извлекаем записи как объекты модели
        records = result.scalars().all()
        if not records:
            logger.warning('Products table is empty')
            raise HTTPException(status_code=404, detail="Нет данных о товарах")
        # автоматическое преобразование модели из БД в модель Pydantic (model_validate)
        return [GetAllProductInfo.model_validate(record) for record in records]

    @db_connection
    async def get_all_products_briefly(self, session: AsyncSession) -> List[NameBrandPrice]:
        """Получение краткой инфы о всех товарах, которые есть в наличии"""
        query = select(Products.id, Products.name, Products.brand, Products.price).filter(Products.sum_count > 0)
        try:
            result = await session.execute(query)
        except SQLAlchemyError as e:
            logger.error(f'Get briefly products error: {e}')
            raise e
        records = result.all()
        if not records:
            logger.warning('Products table is empty')
            raise HTTPException(status_code=404, detail="Нет данных о товарах")
        return [NameBrandPrice.model_validate(record) for record in records]

    @db_connection
    async def get_one_product(self, session: AsyncSession, product_id: int) -> GetProductResponse:
        """Получение инфы о товаре по его id"""
        query = select(Products).filter(Products.id == product_id)  # или where
        try:
            result = await session.execute(query)
        except SQLAlchemyError as e:
            logger.error(f'Get product {product_id} info error: {e}')
            raise e
        record = result.scalar_one_or_none()
        if not record:
            logger.warning(f'No data about product with id {product_id}')
            raise HTTPException(status_code=404, detail="Нет данных о товаре")
        return GetProductResponse.model_validate(record)

    @db_connection
    async def get_by_filters(
            self, session: AsyncSession,
            filter_data: ProductsFilters,
    ) -> List[NameBrandPrice]:
        """Получение товаров по фильтрам"""
        # динамическое построение фильтров
        query = (select(Products).filter(
            Products.sum_count > 0,
            Products.price >= filter_data.price_min,
            Products.price < filter_data.price_max)
        )
        if filter_data.name:
            query = query.filter(Products.name == filter_data.name)
        if filter_data.brand:
            query = query.filter(Products.brand == filter_data.brand)

        try:
            result = await session.execute(query)
        except SQLAlchemyError as e:
            logger.error(f'Filter error: {e}')
            raise e
        records = result.scalars().all()  # если просто несколько столбцов, то scalars не нужен
        if not records:
            raise HTTPException(status_code=404, detail="Нет товаров по вашим фильтрам")
        return [NameBrandPrice.model_validate(record) for record in records]

    @db_connection
    async def update_product_by_id(
            self, session: AsyncSession,
            product_id: int,
            updated_data: Dict[str, Any]
    ) -> GetAllProductInfo:
        """Обновление товара по его id"""
        query = update(Products).filter_by(id=product_id).values(
            **updated_data,
            updated_at=datetime.now()
        ).returning(Products)
        try:
            result = await session.execute(query)
            await session.commit()
        except SQLAlchemyError as e:
            logger.error(f'Update product error: {e}')
            await session.rollback()
            raise e
        record = result.scalar_one_or_none()
        if not record:
            raise HTTPException(status_code=404, detail=f'Товара с id={product_id} не существует')
        return GetAllProductInfo.model_validate(record)

    @db_connection
    async def delete_product_by_id(self, session: AsyncSession, product_id: int) -> str:
        """Удаление товара по его id"""
        try:
            product = await session.get(Products, product_id)
            if product:
                await session.delete(product)
                await session.commit()
                return f"Товар с id={product_id} успешно удален"
            raise HTTPException(status_code=404, detail=f'Товара с id={product_id} не существует')
        except SQLAlchemyError as e:
            logger.error(f'Delete product error: {e}')
            await session.rollback()
            raise e

    @db_connection
    async def delete_all(self, session: AsyncSession) -> str:
        """Удаление всех товаров. Метод только для тестирования"""
        try:
            query = delete(Products)
            await session.execute(query)
            await session.commit()
            return "Все товары удалены"
        except SQLAlchemyError as e:
            logger.error(f'Delete all products error: {e}')
            await session.rollback()
            raise e


def get_products_service() -> ProductsService:
    return ProductsService()
