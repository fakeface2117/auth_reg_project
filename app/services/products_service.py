from typing import List, Dict, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Products
from app.db.pg_session import db_connection


class ProductsService:
    """
    Сервис работы с товарами
    """
    @db_connection
    async def add_product(self, session: AsyncSession, product_data: Dict) -> int:
        new_product = Products(**product_data)
        session.add(new_product)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_product.id

    @db_connection
    async def add_many_products(self, session: AsyncSession, products_data: List[Dict[str, Any]]) -> List[Dict]:
        new_products = [Products(**product_data) for product_data in products_data]
        session.add_all(new_products)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return [{"id_product": row.id} for row in new_products]



def get_products_service() -> ProductsService:
    return ProductsService()
