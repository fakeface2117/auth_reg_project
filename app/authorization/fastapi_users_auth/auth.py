import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from app.authorization.fastapi_users_auth.user_service import get_user_manager
from app.db.models import User
from app.core.config import settings

age_life = 3600

cookie_transport = CookieTransport(cookie_name=settings.COOKIE_NAME, cookie_max_age=age_life)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_AUTH_KEY, lifetime_seconds=age_life)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
