import aiohttp
from fastapi import HTTPException
from starlette import status

from apps.users.exceptions import VerifyEmailException
from core.config import settings


async def verify_email(email: str):
    """
    Проверка почты через стороннее API
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=settings.HUNTER_API_URL + settings.HUNTER_VERIFY_ENDPOINT,
            params={
                "email": email,
                "api_key": settings.HUNTER_API_KEY,
            },
        ) as response:
            content = await response.json()
            if (code := response.status) != status.HTTP_200_OK:
                if code < status.HTTP_400_BAD_REQUEST:
                    raise HTTPException(
                        status_code=code, detail="Please try again later"
                    )
                else:
                    details = content["errors"]["details"]
                    raise HTTPException(status_code=code, detail=details)
            else:
                if content["data"]["status"] not in settings.HUNTER_SUCCESS_STATUSES:
                    raise VerifyEmailException()
