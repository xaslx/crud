from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt

from config.config import settings
from dao.users_dao import UsersDAO
from exceptions import (
    IncorrectTokenException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotAdmin,
    UserIsNotPresentException,
)
from models.user_models import User


def get_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user


async def get_admin_user(user: User = Depends(get_current_user)):
    role = ["admin", "dev"]
    if user.role not in role:
        raise UserIsNotAdmin
    return user
