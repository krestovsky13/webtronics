from pydantic import (
    BaseModel,
    EmailStr,
    validator,
)


class BaseUser(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(BaseUser):
    """
    Создание пользователя
    """

    password: str
    confirm_password: str

    @validator("confirm_password", pre=True)
    def passwords_match(cls, v, values, **kwargs):
        if v != values.get("password"):
            raise ValueError("The two passwords did not match.")
        return v


class ShowUser(BaseUser):
    """
    Просмотр пользователя
    """

    is_active: bool
