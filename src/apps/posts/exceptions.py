from typing import (
    Optional,
    Dict,
    Any,
)
from starlette.exceptions import HTTPException as StarletteHTTPException


class LikeOwnPostException(StarletteHTTPException):
    def __init__(self, headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=403,
            detail="You can't rate your post",
            headers=headers,
        )


class EditOwnPostException(StarletteHTTPException):
    def __init__(self, headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=403,
            detail="You can only edit your posts",
            headers=headers,
        )
