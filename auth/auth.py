from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from config.config import settings
from dao.users_dao import UsersDAO
from exceptions import IncorrectEmailOrPasswordException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(username: str, password: str):
    user = await UsersDAO.find_one_or_none(username=username)
    if not (user and verify_password(password, user.hashed_password)):
        raise IncorrectEmailOrPasswordException
    return user


async def authenticate_user_by_email(email: EmailStr, password: str):
    user_email = await UsersDAO.find_one_or_none(email=email)
    if not (
        user_email and verify_password(password, user_email.hashed_password)
    ):
        raise IncorrectEmailOrPasswordException
    return user_email
