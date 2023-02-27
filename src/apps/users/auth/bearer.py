from typing import Optional

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from core.config import settings


class JWTBearer(HTTPBearer):
    """
    JWT аутентификация
    """

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if await self.verify_jwt(request, credentials.credentials):
                return credentials.credentials
            raise HTTPException(
                status_code=403, detail="Invalid token or expired token."
            )
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    async def verify_jwt(self, request: Request, token: str) -> Optional[bool]:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
        except Exception:
            return
        else:
            username: str = payload.get("username")
            await self.note_user(request, username)

        return True

    @staticmethod
    async def note_user(request: Request, username: str) -> None:
        """
        Запись в запрос текущего пользователя
        """
        request.state.user = username
