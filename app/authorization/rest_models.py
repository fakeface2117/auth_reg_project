from datetime import datetime, date
from typing import Optional
from uuid import UUID

from fastapi_users import schemas


class UserRead(schemas.BaseUser[UUID]):
    id: UUID
    email: str
    registered_at: datetime
    role_id: int
    first_name: str
    last_name: str
    birth_date: date
    sex: str
    contacts: Optional[dict]

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
    email: str
    password: str
    first_name: str
    last_name: str
    birth_date: date
    sex: str

    # username: str
    # email: str
    # password: str
    # role_id: int
    # is_active: Optional[bool] = True
    # is_superuser: Optional[bool] = False
    # is_verified: Optional[bool] = False
