from functools import wraps
from typing import AsyncGenerator, Annotated

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column

from app.core.config import settings

# metadata = MetaData()
# Base = declarative_base(metadata=metadata)
uniq_str_notnull = Annotated[str, mapped_column(unique=True, nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    # @declared_attr.directive
    # def __tablename__(cls) -> str:
    #     return f"{cls.__name__.lower()}s"

if settings.MODE == "TEST":
    DATABASE_URL = settings.DB_CONNECTION_STRING_TEST
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DB_CONNECTION_STRING
    DATABASE_PARAMS = {'future': True, 'echo': False}

pg_engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

SessionLocal = async_sessionmaker(
    bind=pg_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


def db_connection(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with SessionLocal() as session:
            try:
                return await func(*args, session=session, **kwargs)
            except Exception as ex:
                await session.rollback()
                raise ex
            finally:
                await session.close()

    return wrapper
