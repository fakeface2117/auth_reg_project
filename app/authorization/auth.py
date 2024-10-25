# import uuid
#
# from fastapi_users import FastAPIUsers
# from fastapi_users.authentication import CookieTransport, AuthenticationBackend
# from fastapi_users.authentication import JWTStrategy
#
# from app.authorization.user_service import get_user_manager
# from app.authorization.models import User
# from app.core.config import SECRET_AUTH_KEY, COOKIE_NAME
#
# cookie_transport = CookieTransport(cookie_name=COOKIE_NAME, cookie_max_age=3600)
#
#
# def get_jwt_strategy() -> JWTStrategy:
#     return JWTStrategy(secret=SECRET_AUTH_KEY, lifetime_seconds=3600)
#
#
# auth_backend = AuthenticationBackend(
#     name="jwt",
#     transport=cookie_transport,
#     get_strategy=get_jwt_strategy,
# )
#
# fastapi_users = FastAPIUsers[User, uuid.UUID](
#     get_user_manager,
#     [auth_backend],
# )
#
# current_user = fastapi_users.current_user()
