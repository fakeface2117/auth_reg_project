from typing import Union, AsyncGenerator, Annotated

from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column

# metadata = MetaData()
# Base = declarative_base(metadata=metadata)
uniq_str_notnull = Annotated[str, mapped_column(unique=True, nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    # @declared_attr.directive
    # def __tablename__(cls) -> str:
    #     return f"{cls.__name__.lower()}s"


SessionLocal: Union[sessionmaker, None] = None


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
