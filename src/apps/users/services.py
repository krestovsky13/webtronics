from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from apps.users.auth.hashing import Hasher
from db.repository import BaseRepository
from apps.users.models import User
from apps.users.schemas import UserCreate, BaseUser


class UserServices(BaseRepository[User, UserCreate, BaseUser]):
    """
    Класс операций с пользователями
    """

    def __init__(self):
        super().__init__(User)

    async def create(self, obj: UserCreate, db: AsyncSession) -> User:
        """
        Создание пользователя
        """
        # Проверяем наличие пользователя
        user_exist = await db.scalar(
            select(User).filter(
                (User.email == obj.email) | (User.username == obj.username)
            )
        )
        if not user_exist:
            # Хэшируем пароль
            user = User(
                username=obj.username,
                email=obj.email,
                hashed_password=Hasher.get_password_hash(obj.password),
                is_active=True,
                is_superuser=False,
            )

            return await super().create(user, db)

    @staticmethod
    async def get_user_by_username(username: str, db: AsyncSession) -> Optional[User]:
        results = await db.execute(select(User).where(User.username == username))
        if obj := results.one_or_none():
            return obj[0]
