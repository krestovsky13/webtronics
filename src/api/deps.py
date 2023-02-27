from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

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
    user: User = await UserServices.get_user_by_username(
        username=request.state.user,
        db=db,
    )

    return user
