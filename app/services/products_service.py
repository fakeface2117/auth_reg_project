from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Products
from app.decorators.connection_db import db_connection


class ProductsService:
    @db_connection
    async def add_product(self, session: AsyncSession, product_data: dict):
        new_product = Products(
            name=product_data['name'],
            brand=product_data['brand'],
            price=product_data['price'],
            counts=product_data['counts'],
            description=product_data['description']
        )
        session.add(new_product)
        await session.commit()
        return new_product.id

def get_products_service() -> ProductsService:
    return ProductsService()