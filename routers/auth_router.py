from fastapi import APIRouter, Response

from auth.auth import authenticate_user, create_access_token, get_password_hash
from dao.users_dao import UsersDAO
from exceptions import UserAlreadyExistsException, UserNotFound
from schemas.users_schemas import UserAfterRegister, UserLogin, UserRegister
from tasks.tasks import send_user_confirmation_message

router = APIRouter(prefix="/auth", tags=["Аутентификация и Авторизация"])


@router.post("/register")
async def register_user(user: UserRegister) -> UserAfterRegister:
    existing_user_email = await UsersDAO.find_one_or_none(email=user.email)
    existing_user_username = await UsersDAO.find_one_or_none(
        username=user.username
    )

    if existing_user_username or existing_user_email:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user.password)
    user = await UsersDAO.add(
        username=user.username,
        email=user.email,
        date_of_birthday=user.date_of_birthday,
        hashed_password=hashed_password,
    )
    send_user_confirmation_message.delay(user.username, user.email)
    return user


@router.post("/login")
async def login_user(response: Response, user_data: UserLogin):
    user = await authenticate_user(user_data.username, user_data.password)

    if not user:
        raise UserNotFound
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("user_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("user_access_token")
