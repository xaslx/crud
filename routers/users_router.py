import aiofiles
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.templating import Jinja2Templates
from auth.auth import get_password_hash
from auth.dependencies import get_admin_user, get_current_user
from dao.users_dao import UsersDAO
from exceptions import (
    NotAccess,
    UserAlreadyBan,
    UserAlreadyUnBan,
    UserNotFound,
    IncorrectExtension,
    UnverifiedUser,
    FileTooLarge
)
from schemas.users_schemas import UserS
import secrets
from models.user_models import User
from tasks.tasks import save_image


template = Jinja2Templates("templates")


router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("")
async def get_users(user: User = Depends(get_admin_user)) -> list[UserS]:
    return await UsersDAO.find_all()


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)) -> UserS:
    return await UsersDAO.find_one_or_none(id=user.id)


@router.get("/{username}")
async def get_user_by_username(username: str) -> UserS:
    user = await UsersDAO.find_one_or_none(username=username)
    if not user:
        raise UserNotFound
    return user


@router.put("/{user_id}")
async def update_user(
    new_username: str,
    new_email: str,
    new_password: str,
    user: User = Depends(get_current_user),
):
    hashed_password = get_password_hash(new_password)
    return await UsersDAO.update_user(
        user.id,
        username=new_username,
        email=new_email,
        hashed_password=hashed_password,
    )


@router.put("/update/{user_id}")
async def update_role_user(
    user_id: int, new_role: str, user: User = Depends(get_current_user)
):
    user = await UsersDAO.find_one_or_none(id=user_id)
    if not user:
        raise UserNotFound
    return await UsersDAO.update_user(user_id=user.id, role=new_role)


@router.post("/uplod_file")
async def create_upload_file(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
):
    
    filename = file.filename
    extension = filename.split(".")[-1]
    if extension not in ["png", "jpg", "webp"]:
        raise IncorrectExtension
    if not user.is_verified:
        raise UnverifiedUser
    if file.size > 5242880:
        raise FileTooLarge

    FILEPATH = "./static/user_photo/"
    token_name = secrets.token_hex(10) + "." + extension
    generated_name = FILEPATH + token_name

    file_content = await file.read()
    async with aiofiles.open(generated_name, "wb") as file:
        await file.write(file_content)
    save_image.delay(generated_name)
    return await UsersDAO.update_user(user_id=user.id, image_url=token_name)
    


async def check_user(user, user_admin):
    if not user:
        raise UserNotFound
    if user.id == user_admin.id or user.role in ["admin", "dev"]:
        raise NotAccess
    return True


@router.put("/ban")
async def ban_user(username: str, user_admin: User = Depends(get_admin_user)):
    user: User = await UsersDAO.find_one_or_none(username=username)
    if await check_user(user, user_admin):
        if not user.is_banned:
            return await UsersDAO.update_user(user_id=user.id, is_banned=True)
        return UserAlreadyBan


@router.put("/unban")
async def unban_user(
    username: str, user_admin: User = Depends(get_admin_user)
):
    user: User = await UsersDAO.find_one_or_none(username=username)
    if await check_user(user, user_admin):
        if user.is_banned:
            return await UsersDAO.update_user(user_id=user.id, is_banned=False)
        raise UserAlreadyUnBan

