from datetime import datetime, date
from typing import Optional, Any, List, Literal
from uuid import UUID

from fastapi_users import schemas
from pydantic import EmailStr, field_validator, Field, BaseModel

from app.db.sql_enums import SexEnum, RoleEnum


class UserContactsVK(BaseModel):
    contact: Literal['VK']
    value: Any
    @field_validator('value')
    def check_value(cls, value):
        # валидация для ВК
        return value


class UserContactsPHONE(BaseModel):
    contact: Literal['PHONE']
    value: Any
    @field_validator('value')
    def check_value(cls, value):
        # валидация для телефона
        return value

class UserRead(schemas.BaseUser[UUID]):
    # означает, что класс работает с базой
    class Config:
        from_attributes = True

    id: UUID
    email: EmailStr
    registered_at: datetime
    user_role: RoleEnum
    first_name: str
    last_name: str
    birth_date: date
    sex: SexEnum
    contacts: Optional[List[UserContactsVK | UserContactsPHONE]]

    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserCreate(schemas.BaseUserCreate):
    # означает, что класс работает с базой
    class Config:
        from_attributes = True

    email: EmailStr
    password: str
    first_name: str
    last_name: str
    birth_date: date
    sex: SexEnum = Field(..., description='Вариант "man" или "woman"')

    contacts: Optional[List[UserContactsVK | UserContactsPHONE]]

    @field_validator('birth_date')
    def check_birth_date(cls, value):
        if value >= datetime.now().date():
            raise ValueError('Вы не могли родиться в будущем')
        if date(year=value.year + 14, month=value.month, day=value.day) > datetime.now().date():
            raise ValueError('Вам должно быть 14 лет')
        return value


class UserUpdate(schemas.BaseUserUpdate):
    class Config:
        from_attributes = True

    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    contacts: Optional[List[UserContactsVK | UserContactsPHONE]] = None
