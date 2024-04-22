import re
from datetime import date, datetime

from fastapi import HTTPException
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    field_validator,
)


USERNAME_CHECK = re.compile(r"^[a-zA-Z0-9_]{4,15}$")

PASSWORD_CHECK = re.compile(r"^[a-zA-Z0-9_]{6,20}$")


class UserS(BaseModel):
    id: int
    username: str
    email: EmailStr
    registered_at: datetime
    role: str
    image_url: str
    is_banned: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    registered_at: datetime
    role: str

    model_config = ConfigDict(from_attributes=True)


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("username")
    def validate_username(cls, value):
        if not USERNAME_CHECK.match(value):
            raise HTTPException(
                status_code=422,
                detail=f"Имя пользователя должно содержать только [англ.букв, цифры 0-9, знак _], быть минимум 4 символа "
                f"и не должно привышать 15 символов",
            )
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if not PASSWORD_CHECK.match(str(value)):
            raise HTTPException(
                status_code=422,
                detail=f"Пароль должен содержать только [англ.букв, цифры 0-9, знак _], быть минимум 6 символов "
                f"и не должен привышать 20 символов",
            )
        return value


class UserLogin(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)
