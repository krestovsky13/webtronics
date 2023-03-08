from typing import (
    Optional,
    Dict,
    Any,
    TypeVar,
    Type,
)

from starlette.exceptions import HTTPException as StarletteHTTPException

from db.models import BaseModel

Model = TypeVar("Model", bound=BaseModel)


class DoesNotExistException(StarletteHTTPException):
    def __init__(
        self, _id: int, model: Type[Model], headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=404,
            detail=f"{model.__tablename__.title()} with id={_id} does not exist",
            headers=headers,
        )


class AlreadyExistException(StarletteHTTPException):
    def __init__(self, model: Type[Model], headers: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=400,
            detail=f"{model.__tablename__.title()} already exist",
            headers=headers,
        )


class UnauthorizedException(StarletteHTTPException):
    def __init__(self, headers: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=401,
            detail="Incorrect username or password",
            headers=headers,
        )
