from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from core.config import settings


class AsyncDatabaseSession:
    """
    Инициализация асинхронной сессии
    """

    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

    def __init__(self):
        self._engine = create_async_engine(
            self.SQLALCHEMY_DATABASE_URL,
            echo=settings.DEBUG,
        )

        self._session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def get_db(self) -> AsyncSession:
        async with self._session() as session:
            yield session


db = AsyncDatabaseSession()
