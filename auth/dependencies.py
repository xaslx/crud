import inspect

from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import settings
from database.database import get_async_session
from exceptions import (
    IncorrectTokenException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotAdmin,
    UserIsNotPresentException,
)
from models.user_models import User
from repository.users_repository import UsersRepository


def get_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(
    async_db: AsyncSession = Depends(get_async_session),
    token: str = Depends(get_token),
) -> User:

    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    if mod.__name__ == "admin.admin":
        user = await UsersRepository.find_one_or_none_for_admin(
            id=int(user_id)
        )
    else:
        user = await UsersRepository.find_one_or_none(
            id=int(user_id), session=async_db
        )
    if not user:
        raise UserIsNotPresentException
    return user


async def get_admin_user(user: User = Depends(get_current_user)):
    role = ["admin", "dev"]
    if user.role not in role:
        raise UserIsNotAdmin
    return user
