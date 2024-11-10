from sqlalchemy.ext.asyncio import async_sessionmaker


def db_connection(func):
    async def wrapper(*args, **kwargs):
        async with async_sessionmaker() as session:
            try:
                return await func(*args, session=session, **kwargs)
            except Exception as ex:
                await session.rollback()
                raise ex
            finally:
                await session.close()
    return wrapper
