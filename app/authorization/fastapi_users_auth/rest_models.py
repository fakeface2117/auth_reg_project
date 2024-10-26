from datetime import datetime, date
from typing import Optional
from uuid import UUID

from fastapi_users import schemas
from pydantic import EmailStr, field_validator

from app.db.sql_enums import SexEnum, RoleEnum


class UserRead(schemas.BaseUser[UUID]):
    id: UUID
    email: EmailStr
    registered_at: datetime
    # role_id: int
    user_role: str
    first_name: str
    last_name: str
    birth_date: date
    sex: str
    contacts: Optional[dict]

    is_active: bool
    is_superuser: bool
    is_verified: bool

    # id: UUID
    # email: str
    # username: str
    # role_id: int
    # is_active: bool = True
    # is_superuser: bool = False
    # is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    birth_date: date
    sex: SexEnum

    @field_validator('birth_date')
    def check_birth_date(cls, value):
        if value >= datetime.now().date():
            raise ValueError('Вы не могли родиться в будущем')
        if date(year=value.year + 14, month=value.month, day=value.day) > datetime.now().date():
            raise ValueError('Вам должно быть 14 лет')
        return value


# TODO сделать схему и передать ее в параметры
class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None
