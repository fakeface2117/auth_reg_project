import asyncio

# from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
import pytest
from sqlalchemy import insert

from app.core.config import settings
from app.db.pg_session import Base, pg_engine, SessionLocal
from app.db.models import User, Products, Role, StoreBucket, StoreOrders, StoreOrderProducts
from app.tests.testdata.mock_products import products_test_data
from app.main import app as fastapi_app
from app.tests.testdata.mock_roles import roles_test_data
from app.tests.testdata.mock_users import users_test_data


# можно создавать конфтест файлы вглубь директорий
# фикстуры для подготовки среды, отдачи данных, сессий и тд


@pytest.fixture(scope="session", autouse=True)  # значит что на все тесты распространяется
async def setup_db():
    """Создание структуры БД и заполнение ее данными"""
    print(f"DB_URL={settings.DB_CONNECTION_STRING}")
    assert settings.MODE == 'TEST'

    async with pg_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        add_roles = insert(Role).values(roles_test_data)
        add_users = insert(User).values(users_test_data)
        add_products = insert(Products).values(products_test_data)
        await session.execute(add_roles)
        await session.execute(add_users)
        await session.execute(add_products)
        await session.commit()


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def auth_async_client():
    """Асинхронный аутентифицированный клиент для тестирования эндпоинтов"""
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        await ac.post(
            url="/api/store/auth/login",
            data={
                "username": "admin@example.com",
                "password": "1234",
            },
            headers={"content-type": 'application/x-www-form-urlencoded'}
        )
        # assert ac.cookies["access_token"]
        yield ac


@pytest.fixture(scope='function')
async def async_session():
    async with SessionLocal() as session:
        yield session
