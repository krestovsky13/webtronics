from fastapi import (
    APIRouter,
)
from fastapi import (
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import DoesNotExistException
from apps.users.models import User
from apps.users.services import UserServices
from apps.users.schemas import (
    ShowUser,
    BaseUser,
)
from apps.users.auth.bearer import JWTBearer
from core.session import db

router = APIRouter()


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list[ShowUser],
    dependencies=[Depends(JWTBearer())],
)
async def all_users(
    user_services: UserServices = Depends(), db: AsyncSession = Depends(db.get_db)
):
    return await user_services.list(db)


@router.get(
    "/get/{_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowUser,
    dependencies=[Depends(JWTBearer())],
)
async def get_user(
    _id: int,
    user_services: UserServices = Depends(),
    db: AsyncSession = Depends(db.get_db),
):
    if not (user := await user_services.get(_id, db)):
        raise DoesNotExistException(_id, User)

    return user


@router.patch(
    "/update/{_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowUser,
    dependencies=[Depends(JWTBearer())],
)
async def update_user(
    _id: int,
    user_schema: BaseUser,
    user_services: UserServices = Depends(),
    db: AsyncSession = Depends(db.get_db),
):
    if not (user := await user_services.update(_id, user_schema, db)):
        raise DoesNotExistException(_id, User)

    return user


@router.delete(
    "/delete/{id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
async def delete_user(
    _id: int,
    user_services: UserServices = Depends(),
    db: AsyncSession = Depends(db.get_db),
):
    if not (user_id := await user_services.delete(_id, db)):
        raise DoesNotExistException(_id, User)

    return {"msg": f"Successfully deleted (User_id={user_id})"}
