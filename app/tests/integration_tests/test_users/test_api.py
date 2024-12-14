import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,status_code", [
    ("user1@example.com", "1234", 201),
    ("user1@example.com", "4321", 400),
    ("user2@example.com", "1234", 201),
    ("user3example.com", "1234", 422)
])
async def test_register_user(email, password, status_code, async_client: AsyncClient):  # async_client из conftest
    response = await async_client.post("/api/store/auth/register", json={
        "email": email,
        "password": password,
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "first_name": "Человек",
        "last_name": "Паук",
        "birth_date": "2000-12-07",
        "sex": "man",
        "contacts": [
            {
                "contact": "VK",
                "value": "vk_id"
            },
            {
                "contact": "PHONE",
                "value": "88005553535"
            }
        ]
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("username, password, status_code", [
    ("admin@example.com", "1234", 204),
    ("test@example.com", "1234", 204),
    ("admin@example.com", "123", 400),
    ("admin@example.com", None, 422),
])
async def test_login_and_request_user(username, password, status_code,
                                      async_client: AsyncClient):  # async_client из conftest
    response = await async_client.post(
        url="/api/store/auth/login",
        data={
            "username": username,
            "password": password
        } if password else {"username": username},
        headers={"content-type": 'application/x-www-form-urlencoded'}
    )
    assert response.status_code == status_code

    if status_code == 204:
        access_token = response.cookies.get('access_token')
        assert access_token is not None

        protected_response = await async_client.get('/api/store/protected', cookies={'access_token': access_token})
        assert protected_response.status_code == 200
        assert protected_response.json() == f"Hello {username}"


async def test_protected_router(auth_async_client: AsyncClient):
    cookies = {'access_token': auth_async_client.cookies['access_token']}
    protected_response = await auth_async_client.get('/api/store/protected', cookies=cookies)
    assert protected_response.status_code == 200
    assert protected_response.json() == "Hello admin@example.com"
