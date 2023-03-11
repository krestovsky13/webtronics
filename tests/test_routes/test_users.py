import json

from httpx import AsyncClient

from apps.users.auth.jwt import AuthService
from core.config import settings


async def test_create_user(client: AsyncClient):
    data = {
        "username": "user_name",
        "email": "zxc@example.com",
        "password": settings.TEST_USER_PASSWORD,
        "confirm_password": settings.TEST_USER_PASSWORD,
    }
    response = await client.post("/auth/signup", content=json.dumps(data))

    assert response.status_code == 201
    assert response.json()["username"] == data["username"]
    assert response.json()["email"] == data["email"]
    assert response.json()["is_active"] is True


async def test_login_for_access_token(user_jwt_token_headers: dict):
    token = user_jwt_token_headers.get("Authorization").split()[-1]
    payload: dict = await AuthService.get_payload_from_token(token)

    assert payload["username"] == settings.TEST_USER_USERNAME
    assert payload["email"] == settings.TEST_USER_EMAIL
