from fastapi import APIRouter, Response, Request, Depends
from fastapi.responses import JSONResponse

from auth.auth import authenticate_user, create_access_token, get_password_hash
from auth.authentication import generate_token
from auth.dependencies import get_current_user
from dao.users_dao import UsersDAO
from exceptions import UserAlreadyExistsException, UserNotFound
from schemas.users_schemas import UserOut, UserLogin, UserRegister
from tasks.tasks import send_user_confirmation_message, reset_password_email, password_changed
from models.user_models import User
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
import secrets
from logger import logger
from datetime import timedelta

templates = Jinja2Templates('static/templates')
router = APIRouter(prefix="/auth", tags=["Аутентификация и Авторизация"])


@router.post("/register")
async def register_user(user_register: UserRegister):
    existing_user_email: str = await UsersDAO.find_one_or_none(email=user_register.email)
    existing_user_username: str = await UsersDAO.find_one_or_none(username=user_register.username)

    if existing_user_username or existing_user_email:
        raise UserAlreadyExistsException
    hashed_password: str = get_password_hash(user.password)
    user = await UsersDAO.add(
        username=user_register.username,
        email=user_register.email,
        hashed_password=hashed_password,
    )
    logger.info(f'Пользователь {user_register.username} зарегистрировался')
    if user:
        token: str = await generate_token(user)
        send_user_confirmation_message.delay(user.username, user.email, token)
        return JSONResponse(content={'msg': 'Вы успешно зарегистрировались, \
                                    письмо для верификации отправлено вам на почту'})
    return JSONResponse(content={'msg': 'Не удалось зарегистрироваться'})


@router.post("/login")
async def login_user(response: Response, user_data: UserLogin):
    user: User = await authenticate_user(user_data.username, user_data.password)
    if not user:
        raise UserNotFound
    access_token: str = create_access_token({"sub": str(user.id)})
    response.set_cookie("user_access_token", access_token, httponly=True, expires=timedelta(hours=1))
    logger.info(f'Пользователь {user.username} вошел в систему')
    return access_token

@router.post("/send_confirm_email")
async def send_email_confirm(user: User = Depends(get_current_user)):
    token: str = await generate_token(user)
    send_user_confirmation_message.delay(user.username, user.email, token)
    logger.info(f'Пользователь {user.username} запросил письмо с верификацией на почту')
    return JSONResponse(
        content={
            "msg": "Письмо для верификации аккаунта, отправлено на вашу почту"
        }
    )

@router.get("/verification")
async def email_verification(request: Request, token: str):
    user: User = await get_current_user(token)
    if not user.is_verified:
        await UsersDAO.update_user(user_id=user.id, is_verified=True)
        logger.info(f'Пользователь {user.username} верифицировал свой профиль')
        return templates.TemplateResponse(
            "verification.html",
            {"request": request, "username": user.username},
        )
    return templates.TemplateResponse("redirect.html", {"request": request})

@router.post('/forgot_password')
async def forgot_password(email: EmailStr):
    user: User = await UsersDAO.find_one_or_none(email=email)
    if not user:
        raise UserNotFound
    token: str = await generate_token(user)
    reset_password_email.delay(email=user.email, token=token)
    logger.info(f'Пользователю {user.username} направлено письмо для сброса пароля, на почту')
    return JSONResponse(content={'msg': 'Письмо для сброса пароля отправлено вам на почту'})

@router.get('/reset_password')
async def reset_password(token: str):
    user: User = await get_current_user(token)
    new_password: str = secrets.token_hex(10)
    hashed_password: str = get_password_hash(new_password)
    password_changed.delay(user.email, user.username, new_password)
    await UsersDAO.update_user(user_id=user.id, hashed_password=hashed_password)
    logger.info(f'Пользователю {user.username} был сброшен пароль')
    return JSONResponse(content={'msg': 'Ваш пароль сброшен, новый отправлен на вашу почту'})

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("user_access_token")
    