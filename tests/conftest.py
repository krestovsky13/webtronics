import asyncio
from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import settings

from core.session import db
from db.models import BaseModel
from main import start_application
from tests.utils.auth import authentication_token_from_username

engine = create_async_engine(settings.DATABASE_TEST_URL)
test_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
async def test_db_session() -> AsyncSession:
    """
    Тестова сессия БД
    """
    async with test_session() as session:
        yield session


@pytest.fixture(autouse=True, scope="session")
async def app() -> AsyncGenerator[FastAPI, None]:
    """
    Инициализация приложения и тестовых таблиц
    """
    _app = start_application()
    yield _app


@pytest.fixture(autouse=True)
async def init_db():
    """
    Очистка между тестами
    """
    # FIXME
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client(
    app: FastAPI, test_db_session: AsyncSession
) -> AsyncGenerator[AsyncClient, None]:
    """
    Тестовый клиент
    """

    def _get_test_db():
        try:
            yield test_db_session
        finally:
            pass

    # Переопределение зависимости БД сессии для роутинга тестов
    app.dependency_overrides[db.get_db] = _get_test_db

    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000/v1") as client:
        yield client


@pytest.fixture(scope="function")
async def user_jwt_token_headers(client: AsyncClient, test_db_session: AsyncSession):
    """
    Прокидывает токен в тестовые эндпоинты
    """
    return await authentication_token_from_username(client=client, db=test_db_session)
