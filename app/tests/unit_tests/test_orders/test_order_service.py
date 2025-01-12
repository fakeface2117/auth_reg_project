import pytest
from httpx import AsyncClient


class TestOrderService:

    async def test_add_order(self, auth_async_client: AsyncClient):
        cookies = {'access_token': auth_async_client.cookies['access_token']}
        response = await auth_async_client.post(
            url="/api/store/v1/orders/add",
            cookies=cookies
        )
        assert response.status_code == 200
        response_content = response.json()
        assert response_content['total_price'] == 3500
        assert response_content['order_status'] == 'создан'

    async def test_get_user_orders(self, auth_async_client: AsyncClient):
        cookies = {'access_token': auth_async_client.cookies['access_token']}
        response = await auth_async_client.get(
            url="/api/store/v1/orders/user-orders",
            cookies=cookies
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

    @pytest.mark.parametrize("order_id, status_code", [
        (1, 200),
        (111, 404),
    ])
    async def test_get_user_order(self, order_id, status_code, auth_async_client: AsyncClient):
        cookies = {'access_token': auth_async_client.cookies['access_token']}
        response = await auth_async_client.get(
            url=f"/api/store/v1/orders/user-orders/{order_id}",
            cookies=cookies
        )
        assert response.status_code == status_code

        response_json = response.json()
        if status_code == 200:
            assert len(response_json) == 2
        else:
            assert response_json['detail'] == 'Нет данных о заказе'

    @pytest.mark.parametrize("order_id, status_code", [
        (1, 200),
        (111, 404),
    ])
    async def test_buy_order(self, order_id, status_code, auth_async_client: AsyncClient):
        cookies = {'access_token': auth_async_client.cookies['access_token']}
        response = await auth_async_client.post(
            url=f"/api/store/v1/payment/{order_id}",
            cookies=cookies
        )
        assert response.status_code == status_code
        response_json = response.json()
        if response.status_code == 200:
            assert response_json['order_status'] == 'оплачен'
        else:
            assert response_json['detail'] == 'Заказа не существует'

    @pytest.mark.parametrize("order_id, new_status, status_code", [
        (1, 'собирается', 200),
        (111, 'собирается', 404),
        (1, 'другой', 422),
    ])
    async def test_update_order_status(self, order_id, new_status, status_code, auth_async_client: AsyncClient):
        cookies = {'access_token': auth_async_client.cookies['access_token']}
        response = await auth_async_client.patch(
            url=f"/api/store/v1/orders/user-orders/{order_id}",
            cookies=cookies,
            params={'new_status': new_status}
        )
        assert response.status_code == status_code
        response_json = response.json()
        if response.status_code == 200:
            assert response_json['order_status'] == new_status
        if response.status_code == 404:
            assert response_json['detail'] == f"Заказа с id={order_id} не существует"

    @pytest.mark.parametrize("order_status, status_code", [
        ('собирается', 200),
        ('доставлен', 404),
        ('другой', 422)
    ])
    async def test_filter_orders_by_status(self, order_status, status_code, auth_async_client: AsyncClient):
        cookies = {'access_token': auth_async_client.cookies['access_token']}
        response = await auth_async_client.get(
            url=f"/api/store/v1/orders/filer-orders",
            cookies=cookies,
            params={'order_status': order_status}
        )
        assert response.status_code == status_code
        response_json = response.json()
        if response.status_code == 200:
            assert len(response_json) == 1
            assert response_json[0]['order_status'] == order_status
        if response.status_code == 404:
            assert response_json['detail'] == "Нет данных о заказах с таким статусом"
