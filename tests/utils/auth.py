from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users.services import UserServices
from apps.users.schemas import UserCreate
from core.config import settings


async def user_authentication_headers(
    client: AsyncClient, username: str, password: str
) -> dict:
    """
    Возвращает headers с токеном
    """
    data = {"username": username, "password": password}
    r = await client.post("/auth/signin", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    return headers


async def authentication_token_from_username(
    client: AsyncClient,
    db: AsyncSession,
    username: str = settings.TEST_USER_USERNAME,
    email: str = settings.TEST_USER_EMAIL,
    password: str = settings.TEST_USER_PASSWORD,
) -> dict:
    """
    Возвращает токен пользователя, если пользователя нет - создает его
    """
    if not await UserServices.get_user_by_username(username=username, db=db):
        user_schema = UserCreate(
            username=username,
            email=email,
            password=password,
            confirm_password=password,
        )
        await UserServices().create(user_schema, db=db)

    return await user_authentication_headers(
        client=client,
        username=username,
        password=password,
    )
