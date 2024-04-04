import aiofiles
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.templating import Jinja2Templates

from auth.dependencies import get_admin_user, get_current_user
from dao.users_dao import UsersDAO
from exceptions import (
    NotAccess,
    UserAlreadyBan,
    UserAlreadyUnBan,
    UserNotFound,
)
from schemas.users_schemas import User

template = Jinja2Templates("templates")


router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("")
async def get_users(user: User = Depends(get_admin_user)) -> list[User]:
    return await UsersDAO.find_all()


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)) -> User:
    return await UsersDAO.find_one_or_none(id=user.id)


# @router.delete('/{user_id}')
# async def delete_user(user_id: int, user: User = Depends(get_admin_user)):
#     user = await UsersDAO.find_one_or_none(id=user_id)
#     if not user:
#         raise UserNotFound
#     posts = await PostDAO.find_one_or_none(user_id=user.id)
#     if posts:
#         raise PostYetExisting
#     return await UsersDAO.delete(id=user_id)


@router.get("/{username}")
async def get_user_by_username(username: str) -> User:
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
    new_username = new_username
    new_email = new_email
    new_password = new_password
    return await UsersDAO.update_user(
        user.id,
        username=new_username,
        email=new_email,
        hashed_password=new_password,
    )


@router.put("/update/{user_id}")
async def update_role_user(
    user_id: int, new_role: str, user: User = Depends(get_current_user)
):
    user = await UsersDAO.find_one_or_none(id=user_id)
    if not user:
        raise UserNotFound
    return await UsersDAO.update_user(user_id=user.id, role=new_role)


@router.patch("/user_photo")
async def update_photo_profile(
    file: UploadFile = File(), user: User = Depends(get_current_user)
):
    allowed = ["png", "jpg", "webp"]
    file_name = file.filename.split(".")
    if file_name[-1] not in allowed:
        return {"error": "Разрешенные расширения: [png, jpg, webp]"}
    if file.size > 5242880:
        return {"error": "Размер фото не должен превышать 5мб"}
    else:
        async with aiofiles.open(
            f"static/user_photo/{user.id}.webp", "wb+"
        ) as f:
            await f.write(await file.read())
            await UsersDAO.update_user(
                user.id, image_url=f"/static/user_photo/{user.id}"
            )


async def check_user(user, user_admin):
    if not user:
        raise UserNotFound
    if user.id == user_admin.id or user.role in ["admin", "dev"]:
        raise NotAccess
    return True


@router.patch("/ban")
async def ban_user(username: str, user_admin: User = Depends(get_admin_user)):
    user = await UsersDAO.find_one_or_none(username=username)
    if await check_user(user, user_admin):
        if not user.is_banned:
            return await UsersDAO.update_user(user_id=user.id, is_banned=True)
        return UserAlreadyBan


@router.patch("/unban")
async def unban_user(
    username: str, user_admin: User = Depends(get_admin_user)
):
    user = await UsersDAO.find_one_or_none(username=username)
    if await check_user(user, user_admin):
        if user.is_banned:
            return await UsersDAO.update_user(user_id=user.id, is_banned=False)
        raise UserAlreadyUnBan
