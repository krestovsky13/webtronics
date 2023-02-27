from fastapi import APIRouter

from api.v1 import route_users
from api.v1 import route_posts
from api.v1 import route_auth

api_router = APIRouter()

api_router.include_router(route_auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_posts.router, prefix="/posts", tags=["posts"])


def init_router(app):
    """
    Инициализация всех роутов в проекте
    """
    app.include_router(api_router, prefix="/v1")
