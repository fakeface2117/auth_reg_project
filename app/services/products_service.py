from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Products
from db.pg_session import db_connection


class ProductsService:
    @db_connection
    async def add_product(self, session: AsyncSession, product_data: dict):
        new_product = Products(**product_data)
        session.add(new_product)
        await session.commit()
        return new_product.id


def get_products_service() -> ProductsService:
    return ProductsService()
