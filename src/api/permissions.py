from fastapi import (
    Request,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import UnauthorizedException
from apps.posts.exceptions import (
    EditOwnPostException,
    LikeOwnPostException,
)
from apps.users.auth.bearer import JWTBearer
from core.session import db
from apps.users.models import User
from apps.users.services import UserServices


async def authorized_user(
    request: Request,
    db: AsyncSession = Depends(db.get_db),
    token: JWTBearer = Depends(JWTBearer()),
) -> User:
    """
    Аутентифицирует по токену и возвращает авторизованного пользователя
    """
    if not (
        user := await UserServices.get_user_by_username(
            username=request.state.user,
            db=db,
        )
    ):
        raise UnauthorizedException()

    return user


def author_permission(request: Request, user: User = Depends(authorized_user)):
    """
    Permission для авторов
    """
    post_id = int(request.path_params.get("_id"))
    if post_id not in (i.id for i in user.posts):
        raise EditOwnPostException()

    return user


def like_permission(request: Request, user: User = Depends(authorized_user)):
    """
    Permission для лайков/дизлайков
    """
    post_id = int(request.path_params.get("_id"))
    if post_id in (i.id for i in user.posts):
        raise LikeOwnPostException()

    return user
