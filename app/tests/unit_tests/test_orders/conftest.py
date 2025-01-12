import operator

import pytest
from sqlalchemy import insert, select

from app.db.models import StoreBucket, User
from app.db.pg_session import SessionLocal
from app.tests.testdata.mock_bucket import bucket_test_data


@pytest.fixture(scope='session', autouse=True)
async def set_bucket():
    async with SessionLocal() as session:
        user_result = await session.execute(select(User.id).where(User.email == "admin@example.com"))
        user_id = str(user_result.scalar_one_or_none())
        for item in bucket_test_data:
            item.update({'user_id': user_id})
        add_bucket = insert(StoreBucket).values(bucket_test_data)
        await session.execute(add_bucket)
        await session.commit()