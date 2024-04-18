from datetime import datetime, timedelta

from jose import ExpiredSignatureError, JWTError, jwt

from config.config import settings
from dao.users_dao import UsersDAO
from exceptions import (
    IncorrectTokenException,
    TokenExpiredException,
    UserIsNotPresentException,
    UserNotFound,
)
from models.user_models import User


async def verify_token(token: str):
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
        raise UserNotFound
    return user


async def generate_token(user: User):
    expire = datetime.utcnow() + timedelta(minutes=5)
    user_to_email = {"sub": str(user.id), "exp": expire}
    token = jwt.encode(user_to_email, settings.SECRET_KEY, settings.ALGORITHM)
    return token
