from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from auth.auth import (
    authenticate_user_by_email,
    create_access_token,
)
from auth.dependencies import get_current_user
from models.user_models import User


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        role: list = ["admin", "dev"]
        user: User = await authenticate_user_by_email(username, password)
        if user and user.role in role:
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        user: User = await get_current_user(token)
        if not user:
            return False
        return True


authentication_backend = AdminAuth(secret_key="...")
