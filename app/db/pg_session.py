from typing import Union, AsyncGenerator, Annotated

from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column

from core.config import settings

# metadata = MetaData()
# Base = declarative_base(metadata=metadata)
uniq_str_notnull = Annotated[str, mapped_column(unique=True, nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    # @declared_attr.directive
    # def __tablename__(cls) -> str:
    #     return f"{cls.__name__.lower()}s"


pg_engine = create_async_engine(
    url=settings.DB_CONNECTION_STRING,
    future=True,
    echo=False
)

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
