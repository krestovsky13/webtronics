from typing import Optional
from datetime import (
    timedelta,
    datetime,
)

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users.auth.hashing import Hasher
from core.config import settings
from apps.users.services import (
    User,
    UserServices,
)


class AuthService:
    """
    Класс аутентификации модели пользователя
    """

    @staticmethod
    async def authenticate_user(
        username: str, password: str, db: AsyncSession
    ) -> Optional[User]:
        user: User = await UserServices.get_user_by_username(username=username, db=db)
        if user and Hasher.verify_password(password, user.hashed_password):
            return user

    @staticmethod
    async def set_token_payload(user: User, expires_delta: timedelta, **kwargs):
        """
        Полезная нагрузка токена
        """
        # c utcnow неудобно тестить
        expire = datetime.now() + expires_delta

        token_payload = dict(
            username=user.username,
            email=user.email,
            iss="krestovsky",
            sub="auth",
            iat=datetime.timestamp(datetime.now()),
            exp=datetime.timestamp(expire),
            **kwargs
        )

        return token_payload

    @staticmethod
    async def get_payload_from_token(
        token: str,
        secret_key: str = settings.SECRET_KEY,
        algorithms: str | list = settings.ALGORITHM,
    ) -> dict:
        return jwt.decode(token, secret_key, algorithms=algorithms)

    @staticmethod
    async def create_access_token(
        user: User,
        expires_delta: Optional[timedelta] = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    ) -> str:
        token_payload = await AuthService.set_token_payload(
            user=user, expires_delta=expires_delta
        )

        access_token = jwt.encode(
            claims=token_payload,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

        return access_token

    @staticmethod
    async def create_refresh_token(
        user: User,
        expires_delta: Optional[timedelta] = timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        ),
    ) -> str:
        token_payload = await AuthService.set_token_payload(
            user=user, expires_delta=expires_delta
        )

        refresh_token = jwt.encode(
            claims=token_payload,
            key=settings.REFRESH_SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

        return refresh_token
