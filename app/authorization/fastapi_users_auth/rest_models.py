import enum
from datetime import datetime, date
from typing import Optional, Any, List
from uuid import UUID

from fastapi_users import schemas
from pydantic import EmailStr, field_validator, Field, BaseModel

from app.db.sql_enums import SexEnum, RoleEnum

class ContactsEnum(str, enum.Enum):
    VK = "VK"
    OK = "OK"
    PHONE = "PHONE"
    EMAIL = "EMAIL"

class UserContacts(BaseModel):
    contact: ContactsEnum
    value: Any # TODO доп валидация для контактов

    @field_validator('value')
    def check_value(cls, value):
        if cls.contact == "VK":
            raise ValueError('Вы ввели VK')
        if cls.contact == "OK":
            raise ValueError('Вы ввели OK')
        return value

class UserContactsVK(BaseModel):
    contact: str = "VK"
    value: Any # TODO доп валидация для VK
    @field_validator('value')
    def check_value(cls, value):
        return value

class UserContactsOK(BaseModel):
    contact: str = "OK"
    value: Any # TODO доп валидация для OK
    @field_validator('value')
    def check_value(cls, value):
        return value

class UserContactsPHONE(BaseModel):
    contact: str = "PHONE"
    value: Any # TODO доп валидация для телефона
    @field_validator('value')
    def check_value(cls, value):
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
    contacts: Optional[List[UserContactsVK | UserContactsOK | UserContactsPHONE]]

    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserCreate(schemas.BaseUserCreate):
    class Config:
        from_attributes = True

    email: EmailStr
    password: str
    first_name: str
    last_name: str
    birth_date: date
    sex: SexEnum = Field(..., description='Вариант "man" или "woman"')

    contacts: Optional[List[UserContactsVK | UserContactsOK | UserContactsPHONE]] # TODO сделать контакты

    @field_validator('birth_date')
    def check_birth_date(cls, value):
        if value >= datetime.now().date():
            raise ValueError('Вы не могли родиться в будущем')
        if date(year=value.year + 14, month=value.month, day=value.day) > datetime.now().date():
            raise ValueError('Вам должно быть 14 лет')
        return value


# TODO сделать схему и передать ее в параметры
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
