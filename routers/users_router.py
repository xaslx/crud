import secrets

import aiofiles
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_password_hash
from auth.dependencies import get_admin_user, get_current_user
from database.database import get_async_session
from exceptions import (
    FileTooLarge,
    IncorrectExtension,
    NotAccess,
    UnverifiedUser,
    UserAlreadyBan,
    UserAlreadyUnBan,
    UserNotFound,
)
from logger import logger
from models.user_models import User
from repository.users_repository import UsersRepository
from schemas.users_schemas import UserOut
from tasks.tasks import save_image

template = Jinja2Templates("templates")


router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("")
async def get_users(
    user: User = Depends(get_admin_user),
    async_db: AsyncSession = Depends(get_async_session),
) -> list[UserOut]:
    return await UsersRepository.find_all(session=async_db)


@router.get("/me")
async def get_me(
    user: User = Depends(get_current_user),
    async_db: AsyncSession = Depends(get_async_session),
) -> UserOut:
    return await UsersRepository.find_one_or_none(id=user.id, session=async_db)


@router.get("/{username}")
async def get_user_by_username(
    username: str, async_db: AsyncSession = Depends(get_async_session)
) -> UserOut:
    user = await UsersRepository.find_one_or_none(
        username=username, session=async_db
    )
    if not user:
        raise UserNotFound
    return user


@router.put("/{user_id}")
async def update_user(
    new_username: str,
    new_password: str,
    user: User = Depends(get_current_user),
    async_db: AsyncSession = Depends(get_async_session),
):

    hashed_password: str = get_password_hash(new_password)

    updated_info = await UsersRepository.update_user(
        user.id,
        username=new_username,
        hashed_password=hashed_password,
        session=async_db,
    )
    logger.info(
        f"Пользователь {user.username} обновил свои данные на : [username: {new_username}, password: {new_password}]"
    )
    return updated_info


@router.put("/update/{user_id}")
async def update_role_user(
    user_id: int,
    new_role: str,
    user_admin: User = Depends(get_admin_user),
    async_db: AsyncSession = Depends(get_async_session),
):
    user = await UsersRepository.find_one_or_none(id=user_id, session=async_db)
    if not user:
        raise UserNotFound
    updated_role = await UsersRepository.update_user(
        user_id=user.id, role=new_role, session=async_db
    )
    logger.info(
        f"Администратор {user_admin.username} изменил роль пользователю {user.username}"
    )
    return updated_role


@router.post("/uplod_file")
async def upload_photo(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    async_db: AsyncSession = Depends(get_async_session),
):

    filename: str = file.filename
    extension: str = filename.split(".")[-1]
    if extension not in ["png", "jpg", "webp"]:
        raise IncorrectExtension
    if not user.is_verified:
        raise UnverifiedUser
    if file.size > 5242880:
        raise FileTooLarge

    FILEPATH: str = "./static/user_photo/"
    token_name: str = secrets.token_hex(10) + "." + extension
    generated_name: str = FILEPATH + token_name

    file_content = await file.read()
    async with aiofiles.open(generated_name, "wb") as file:
        await file.write(file_content)
    save_image.delay(generated_name)
    updated_photo = await UsersRepository.update_user(
        user_id=user.id, image_url=token_name, session=async_db
    )
    logger.info(f"Пользователь {user.username} обновил свое фото")
    return updated_photo


async def check_user(user, user_admin):
    if not user:
        raise UserNotFound
    if user.id == user_admin.id or user.role in ["admin", "dev"]:
        raise NotAccess
    return True


@router.patch("/ban")
async def ban_user(
    username: str,
    user_admin: User = Depends(get_admin_user),
    async_db: AsyncSession = Depends(get_async_session),
):
    user = await UsersRepository.find_one_or_none(
        username=username, session=async_db
    )
    if await check_user(user, user_admin):
        if not user.is_banned:
            ban_user = await UsersRepository.update_user(
                user_id=user.id, is_banned=True, session=async_db
            )
            logger.info(
                f"Администратор {user_admin.username} заблокировал пользователя: {user.username}"
            )
            return ban_user
        return UserAlreadyBan


@router.patch("/unban")
async def unban_user(
    username: str,
    user_admin: User = Depends(get_admin_user),
    async_db: AsyncSession = Depends(get_async_session),
):
    user = await UsersRepository.find_one_or_none(
        username=username, session=async_db
    )
    if await check_user(user, user_admin):
        if user.is_banned:
            unban_user = await UsersRepository.update_user(
                user_id=user.id, is_banned=False, session=async_db
            )
            logger.info(
                f"Администратор {user_admin.username} разблокировал пользователя: {user.username}"
            )
            return unban_user
        raise UserAlreadyUnBan
