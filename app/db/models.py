import uuid
from datetime import datetime, date
from typing import Text, List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey, text, types, func, JSON, DateTime, ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.pg_session import Base, uniq_str_notnull
from app.db.sql_enums import SexEnum, OrderStatusEnum, RoleEnum


# ForeignKey показывает связь между таблицами
# relationship реализует эти связи в orm

class Role(Base):
    """Таблица ролей"""
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[RoleEnum]

    # на одну роль приходится иного пользователей
    user: Mapped[list["User"]] = relationship(
        "User",
        back_populates="role",
        cascade="all, delete-orphan"  # Удаляет пользователей при удалении роли
    )


class User(SQLAlchemyBaseUserTableUUID, Base):
    """Таблица пользователей"""
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    email: Mapped[uniq_str_notnull]
    registered_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        # default=datetime.utcnow,
        server_default=func.now()
    )  # server_default=func.now()
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    hashed_password: Mapped[str]

    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[date]  # = mapped_column(DateTime(timezone=False), nullable=False)
    sex: Mapped[SexEnum]
    contacts: Mapped[dict | None] = mapped_column(JSON)

    is_active: Mapped[bool]
    is_superuser: Mapped[bool]
    is_verified: Mapped[bool]

    # на одного пользователя приходится несколько товаров в корзине
    bucket_store: Mapped[list["StoreBucket"]] = relationship(
        "StoreBucket",
        back_populates="user",
        cascade="all, delete-orphan"  # Удаляет товары из корзины при удалении пользователя
    )
    # на одного пользователя приходится несколько заказов
    order_store: Mapped[list["StoreOrders"]] = relationship(
        "StoreOrders",
        back_populates="user",
        cascade="all, delete-orphan"  # Удаляет заказы при удалении пользователя
    )
    # одному пользователю соответствует одна  роль
    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="user",
        lazy="joined"  # При подгрузке пользака также подгрузится строчка из роли
    )

    # Связь один к одному
    # profile: Mapped["Profile"] = relationship(
    #     "Profile",
    #     back_populates="user", # указывает на атрибут обратной связи в модели Profile
    #     uselist=False, # Определяет что связь не является списком (по умолчанию список)
    #     lazy="joined" # автоматически подгружает профиль при вызове users # TODO попробовать если что
    # )


class Products(Base):
    """Таблица имеющихся товаров"""
    __tablename__ = "store_products"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, server_default=func.now())
    updated_at: Mapped[datetime | None]
    name: Mapped[str] = mapped_column(nullable=False, unique=False)
    brand: Mapped[str] = mapped_column(nullable=True, unique=False)
    price: Mapped[int] = mapped_column(nullable=False, unique=False, default=0)
    counts: Mapped[dict | None] = mapped_column(JSON)
    parameters: Mapped[dict | None] = mapped_column(JSON)
    description: Mapped[Text]
    # photo_urls: Mapped[List[str] | None] = mapped_column(ARRAY(String)) # TODO в будущем добавить колонку для картинок

    # одному товару соответствует много записей в корзине
    bucket_store: Mapped[list["StoreBucket"]] = relationship(
        "StoreBucket",
        back_populates="product",
        # cascade="all, delete-orphan"
    )
    # одному товару соответствует много записей в заказах
    order_product: Mapped[list["StoreOrderProducts"]] = relationship(
        "StoreOrderProducts",
        back_populates="product",
        # cascade="all, delete-orphan"
    )


class StoreBucket(Base):
    """Корзина. Их не может быть много, поэтому хранит в каждой записи просто данные о товаре"""
    __tablename__ = "store_bucket"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("store_products.id"), nullable=False)
    added_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, server_default=func.now())

    # Одна запись в корзине имеет одну запись о пользователе
    user: Mapped["User"] = relationship(
        "User",
        back_populates="bucket_store"
    )
    # Одна запись в корзине имеет одну запись о товаре
    product: Mapped["Products"] = relationship(
        "Products",
        back_populates="bucket_store"
    )

    # преобразование в словарь для удобства (просто пример)
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "added_at": self.added_at
        }


class StoreOrders(Base):
    """Таблица заказов. Их может быть много, поэтому ссылается на таблицу StoreOrderProducts"""
    __tablename__ = "store_orders"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    order_date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, server_default=func.now())
    order_status: Mapped[OrderStatusEnum] = mapped_column(default=OrderStatusEnum.CREATED)

    # одна запись о заказе имеет одну запись о пользователе
    user: Mapped["User"] = relationship(
        "User",
        back_populates="order_store"
    )

    # одна запись о заказе имеет несколько записей о заказанных товарах
    order_product: Mapped[list["StoreOrderProducts"]] = relationship(
        "StoreOrderProducts",
        back_populates="order",
        # cascade="all, delete-orphan"
    )


class StoreOrderProducts(Base):
    """Таблица товаров в одном заказе"""
    __tablename__ = "store_order_products"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("store_orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("store_products.id"), nullable=False)
    product_name: Mapped[str] = mapped_column(nullable=False)
    product_price: Mapped[int] = mapped_column(nullable=False)
    product_count: Mapped[int] = mapped_column(nullable=False, default=1)

    # одна запись в таблице заказов связана с одним заказом
    order: Mapped["StoreOrders"] = relationship(
        "StoreOrders",
        back_populates="order_product"
    )

    # одна запись о заказанном товаре имеет одну запись о товаре
    product: Mapped["Products"] = relationship(
        "Products",
        back_populates="order_product"
    )
