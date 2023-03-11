import json

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.config import settings
from tests.utils.auth import authentication_token_from_username

post_data = {
    "title": "Webtronics",
    "description": "ZXC",
}
post_data2 = {
    "title": "Yandex",
    "description": "sos",
}


async def test_create_post(client: AsyncClient, user_jwt_token_headers: dict):
    global post_data

    response = await client.post(
        "/posts/create", content=json.dumps(post_data), headers=user_jwt_token_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == post_data["title"]
    assert response.json()["description"] == post_data["description"]


async def test_all_posts(client: AsyncClient, user_jwt_token_headers: dict):
    global post_data
    global post_data2

    await client.post(
        "/posts/create", content=json.dumps(post_data), headers=user_jwt_token_headers
    )
    await client.post(
        "/posts/create", content=json.dumps(post_data2), headers=user_jwt_token_headers
    )

    response = await client.get("/posts/all", headers=user_jwt_token_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]
    assert response.json()[1]


async def test_get_post(client: AsyncClient, user_jwt_token_headers: dict):
    global post_data
    await client.post(
        "/posts/create", content=json.dumps(post_data), headers=user_jwt_token_headers
    )

    response = await client.get("/posts/get/1", headers=user_jwt_token_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == post_data["title"]


async def test_update_post(client: AsyncClient, user_jwt_token_headers: dict):
    global post_data
    global post_data2

    await client.post(
        "/posts/create", content=json.dumps(post_data), headers=user_jwt_token_headers
    )

    response = await client.patch(
        "/posts/update/1",
        content=json.dumps(post_data2),
        headers=user_jwt_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == post_data2["title"]

    response = await client.get("/posts/get/1", headers=user_jwt_token_headers)
    assert response.json()["title"] == post_data2["title"]


async def test_delete_post(client: AsyncClient, user_jwt_token_headers: dict):
    global post_data

    await client.post(
        "/posts/create", content=json.dumps(post_data), headers=user_jwt_token_headers
    )
    post_id = 1

    response = await client.delete(
        f"/posts/delete/{post_id}", headers=user_jwt_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": f"Successfully deleted (Post_id={post_id})"}

    response = await client.get("/jobs/get/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


#
#
async def test_like_post(
    client: AsyncClient, test_db_session: AsyncSession, user_jwt_token_headers: dict
):
    global post_data
    global post_data2

    headers2: dict = await authentication_token_from_username(
        client=client,
        db=test_db_session,
        username="user_name",
        email="zxc@example.com",
        password=settings.TEST_USER_PASSWORD,
    )

    await client.post(
        "/posts/create", content=json.dumps(post_data), headers=user_jwt_token_headers
    )

    response = await client.post("/posts/like/1", headers=headers2)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["like_count"] == 1

    response = await client.post("/posts/like/1", headers=headers2)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["like_count"] == 0
