import functools
from fastapi import HTTPException


def admin_verified(func):
    @functools.wraps(func)
    async def check_admin(*args, **kwargs):
        user = kwargs['user']
        if user.role_id != 3:
            raise HTTPException(status_code=403, detail='Вы не являетесь администратором')
        result = await func(*args, **kwargs)
        return result
    return check_admin