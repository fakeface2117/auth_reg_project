import uuid
from datetime import datetime
from typing import Text

from sqlalchemy import ForeignKey, text, types, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.pg_session import Base, uniq_str_notnull
from app.db.sql_enums import SexEnum, OrderStatusEnum


# ForeignKey показывает связь между таблицами
# relationship реализует эти связи в orm

class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[uniq_str_notnull]

    user: Mapped[list["User"]] = relationship(
        "User",
        back_populates="role",
        cascade="all, delete-orphan"  # Удаляет пользователей при удалении роли
    )


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    email: Mapped[uniq_str_notnull]
    registered_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now()
    )  # server_default=func.now()
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    hashed_password: Mapped[str]

    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[datetime] = mapped_column(nullable=False)
    sex: Mapped[SexEnum]
    contacts: Mapped[dict | None] = mapped_column(JSON)

    bucket_store: Mapped[list["StoreBucket"]] = relationship(
        "StoreBucket",
        back_populates="user",
        cascade="all, delete-orphan"  # Удаляет товары из корзины при удалении пользователя
    )
    order_store: Mapped[list["StoreOrders"]] = relationship(
        "StoreOrders",
        back_populates="user",
        cascade="all, delete-orphan"  # Удаляет заказы при удалении пользователя
    )

    role: Mapped[list["Role"]] = relationship(
        "Role",
        back_populates="user",
    )

    # Связь один к одному
    # profile: Mapped["Profile"] = relationship(
    #     "Profile",
    #     back_populates="user", # указывает на атрибут обратной связи в модели Profile
    #     uselist=False, # Определяет что связь не является списком (по умолчанию список)
    #     lazy="joined" # автоматически подгружает профиль при вызове users # TODO попробоавть если что
    # )


class Products(Base):
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

    bucket_store: Mapped[list["StoreBucket"]] = relationship(
        "StoreBucket",
        back_populates="product",
        # cascade="all, delete-orphan"
    )
    order_product: Mapped[list["StoreOrderProducts"]] = relationship(
        "StoreOrderProducts",
        back_populates="product",
        # cascade="all, delete-orphan"
    )


class StoreBucket(Base):
    """Корзина"""
    __tablename__ = "store_bucket"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("store_products.id"), nullable=False)
    added_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, server_default=func.now())

    user: Mapped["User"] = relationship(
        "User",
        back_populates="bucket_store"
    )
    product: Mapped["Products"] = relationship(
        "Products",
        back_populates="bucket_store"
    )


class StoreOrders(Base):
    """Таблица заказов"""
    __tablename__ = "store_orders"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    order_date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, server_default=func.now())
    order_status: Mapped[OrderStatusEnum] = mapped_column(default=OrderStatusEnum.CREATED)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="order_store"
    )
    order_product: Mapped[list["StoreOrderProducts"]] = relationship(
        "StoreOrderProducts",
        back_populates="order",
        # cascade="all, delete-orphan"
    )


class StoreOrderProducts(Base):
    """Товары в заказе"""
    __tablename__ = "store_order_products"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("store_orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("store_products.id"), nullable=False)
    product_name: Mapped[str] = mapped_column(nullable=False)
    product_price: Mapped[int] = mapped_column(nullable=False)
    product_count: Mapped[int] = mapped_column(nullable=False, default=1)

    order: Mapped["StoreOrders"] = relationship(
        "StoreOrders",
        back_populates="order_product"
    )
    product: Mapped["Products"] = relationship(
        "Products",
        back_populates="order_product"
    )
