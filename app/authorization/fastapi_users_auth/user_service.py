from typing import Optional
from uuid import UUID

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, exceptions, models, schemas, UUIDIDMixin

from app.db.models import User
from app.authorization.fastapi_users_auth.utils import get_user_db

from app.core.config import settings
from app.services.email_service import get_email, EmailService


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = settings.SECRET_AUTH_KEY
    verification_token_secret = settings.SECRET_AUTH_KEY

    def __init__(self, user_db, email_service):
        super().__init__(user_db)
        self.email_service: EmailService = email_service

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        # await self.email_service.send_register_message(to_addr=user.email, to_name=user.first_name)
        print(f"User {user.id} has registered.")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )

        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        created_user.user_role = created_user.role.role
        return created_user

    async def get(self, id: models.ID) -> models.UP:
        """
        Get a user by id.

        :param id: Id. of the user to retrieve.
        :raises UserNotExists: The user does not exist.
        :return: A user.
        """
        user = await self.user_db.get(id)

        if user is None:
            raise exceptions.UserNotExists()

        user.user_role = user.role.role
        return user


async def get_user_manager(user_db=Depends(get_user_db), email_service=Depends(get_email)):
    yield UserManager(user_db, email_service)

# TODO без рассылки на почту
# from typing import Optional
# from uuid import UUID
#
# from fastapi import Depends, Request
# from fastapi_users import BaseUserManager, exceptions, models, schemas, UUIDIDMixin
#
# from app.db.models import User
# from app.authorization.fastapi_users_auth.utils import get_user_db
#
# from app.core.config import settings
#
#
# class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
#     reset_password_token_secret = settings.SECRET_AUTH_KEY
#     verification_token_secret = settings.SECRET_AUTH_KEY
#
#     async def on_after_register(self, user: User, request: Optional[Request] = None):
#         print(f"User {user.id} has registered.")
#
#     async def create(
#             self,
#             user_create: schemas.UC,
#             safe: bool = False,
#             request: Optional[Request] = None,
#     ) -> models.UP:
#         await self.validate_password(user_create.password, user_create)
#
#         existing_user = await self.user_db.get_by_email(user_create.email)
#         if existing_user is not None:
#             raise exceptions.UserAlreadyExists()
#
#         user_dict = (
#             user_create.create_update_dict()
#             if safe
#             else user_create.create_update_dict_superuser()
#         )
#
#         password = user_dict.pop("password")
#         user_dict["hashed_password"] = self.password_helper.hash(password)
#         user_dict["role_id"] = 1
#
#         created_user = await self.user_db.create(user_dict)
#
#         await self.on_after_register(created_user, request)
#
#         created_user.user_role = created_user.role.role
#         return created_user
#
#     async def get(self, id: models.ID) -> models.UP:
#         """
#         Get a user by id.
#
#         :param id: Id. of the user to retrieve.
#         :raises UserNotExists: The user does not exist.
#         :return: A user.
#         """
#         user = await self.user_db.get(id)
#
#         if user is None:
#             raise exceptions.UserNotExists()
#
#         user.user_role = user.role.role
#         return user
#
#
# async def get_user_manager(user_db=Depends(get_user_db)):
#     yield UserManager(user_db)
