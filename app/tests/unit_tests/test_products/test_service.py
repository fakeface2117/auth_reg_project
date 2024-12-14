from contextlib import nullcontext
from numbers import Integral

import pytest
from fastapi import HTTPException

from app.api.v1.products.rest_models import ProductsFilters
from app.services.products_service import ProductsService
from app.tests.testdata.mock_products import products_test_data


class TestProductsService:
    products_service = ProductsService()

    @pytest.mark.parametrize("product_id, name, brand, price, expect", [
        (1, "куртка", "puma", 1000, nullcontext()),
        (2, "футболка", "adidas", 1500, nullcontext()),
        (3, "джинсы", "levis", 2000, pytest.raises(HTTPException))
    ])
    async def test_get_one_product(self, product_id: int, name: str, brand: str, price: int, expect):
        with expect:
            product = await self.products_service.get_one_product(product_id=product_id)
            assert product.id == product_id
            assert product.name == name
            assert product.brand == brand
            assert product.price == price

    async def test_get_all_products(self):
        products = await self.products_service.get_all_products()
        assert len(products) == 2

    async def test_get_all_briefly(self):
        products_briefly = await self.products_service.get_all_products_briefly()
        assert len(products_briefly) == 2

        for i, one_product in enumerate(products_briefly, 1):
            assert one_product.id == products_test_data[i - 1].get('id')
            assert one_product.name == products_test_data[i - 1].get('name')
            assert one_product.brand == products_test_data[i - 1].get('brand')
            assert one_product.price == products_test_data[i - 1].get('price')

    async def test_add_product(self):
        added_product = {
            "id": 10,
            "name": "футболка",
            "brand": "nike",
            "price": 1000,
            "sum_count": 10,
            "counts": [
                {
                    "size": "XS",
                    "count": 5
                }, {
                    "size": "S",
                    "count": 5
                }
            ],
            "description": "описание",
            "parameters": {
                "color": "red",
                "style": "sport",
                "season": "winter"
            }
        }
        product_id = await self.products_service.add_product(product_data=added_product)
        assert isinstance(product_id, Integral)
        assert product_id == added_product['id']

    @pytest.mark.parametrize('filter_data, expect', [
        (ProductsFilters(brand='adidas'), nullcontext()),
        (ProductsFilters(brand='asics'), pytest.raises(HTTPException))
    ])
    async def test_get_by_filters(self, filter_data: ProductsFilters, expect: nullcontext):
        with expect:
            res = await self.products_service.get_by_filters(filter_data=filter_data)
            assert len(res) == 1

    @pytest.mark.parametrize('product_id, expect', [
        (1, nullcontext()),
        (222, pytest.raises(HTTPException))
    ])
    async def test_delete_product_by_id(self, product_id: int, expect: nullcontext):
        with expect:
            result = await self.products_service.delete_product_by_id(product_id=product_id)
            assert result == f"Товар с id={product_id} успешно удален"



