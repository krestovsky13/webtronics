from fastapi.security import OAuth2PasswordRequestForm
from fastapi import (
    Depends,
    APIRouter,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import (
    AlreadyExistException,
    UnauthorizedException,
)
from apps.users.auth.schemas import Token
from apps.users.auth.jwt import AuthService
from apps.users.auth.utils import verify_email
from apps.users.exceptions import VerifyEmailException
from apps.users.models import User
from apps.users.schemas import (
    UserCreate,
    ShowUser,
)
from apps.users.services import UserServices
from core.session import db

router = APIRouter()


@router.post(
    "/signup",
    response_model=ShowUser,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_schema: UserCreate,
    user_services: UserServices = Depends(),
    db: AsyncSession = Depends(db.get_db),
):
    if await verify_email(user_schema.email):
        if user := await user_services.create(user_schema, db):
            return user
        else:
            raise AlreadyExistException(User)
    else:
        raise VerifyEmailException()


@router.post(
    "/signin",
    response_model=Token,
    status_code=status.HTTP_202_ACCEPTED,
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_services: AuthService = Depends(),
    db: AsyncSession = Depends(db.get_db),
):
    user = await auth_services.authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=db,
    )
    if not user:
        raise UnauthorizedException()

    tokens = Token(
        access_token=await auth_services.create_access_token(user=user),
        refresh_token=await auth_services.create_refresh_token(user=user),
        token_type="Bearer",
    )

    return tokens
