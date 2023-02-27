from typing import (
    Optional,
    Dict,
    Any,
)

from starlette.exceptions import HTTPException as StarletteHTTPException


class VerifyEmailException(StarletteHTTPException):
    def __init__(self, headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=422,
            detail="Failed to verify the email address",
            headers=headers,
        )
