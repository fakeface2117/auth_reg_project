import pytest
from httpx import AsyncClient

class TestBucketService:
    @pytest.mark.parametrize("product_id, product_count, product_size, status_code", [
        (1, 2, "XS", 200),
        (2, 50, "XS", 404),
        (100, 2, "XS", 404),
    ])
    async def test_post_user_bucket(self, product_id, product_count, product_size, status_code, auth_async_client: AsyncClient):
        cookies = {'access_token': auth_async_client.cookies['access_token']}
        response = await auth_async_client.post(
            url="/api/store/v1/buckets/postBucketOfUser",
            json={
                "product_id": product_id,
                "product_count": product_count,
                "product_size": product_size
            },
            cookies=cookies
        )
        assert response.status_code == status_code

    async def test_get_bucket(self, auth_async_client: AsyncClient):
        cookies = {'access_token': auth_async_client.cookies['access_token']}
        response = await auth_async_client.get(
            url="/api/store/v1/buckets/getBucketOfUser",
            cookies=cookies
        )
        assert response.status_code == 200

    @pytest.mark.parametrize("product_size, status_code", [
        ("XS", 200),
        ("xs", 422)
    ])
    async def test_delete_item(self, product_size, status_code, auth_async_client: AsyncClient):
        cookies = {'access_token': auth_async_client.cookies['access_token']}
        response = await auth_async_client.delete(
            url="/api/store/v1/buckets/deleteBucketOfUser",
            params={
                "product_id": 1,
                "product_size": product_size
            },
            cookies=cookies
        )
        assert response.status_code == status_code