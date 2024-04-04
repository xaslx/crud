from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


# Пользователи
class UserAlreadyExistsException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь уже существует'

class IncorrectEmailOrPasswordException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверный email или пароль'

class IncorrectEmailOrPasswordExceptionNotEn(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Email или пароль должны быть на английском'

class UserNotFound(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь не найден'

class UserIsNotPresentException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED

class UserIsNotAdmin(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Доступ запрещен'

class UserAlreadyUnBan(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь уже разблокирован'

class UserAlreadyBan(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь уже заблокирован'

class NotAccess(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Не достаточно прав'

class WrongDate(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Дата не должна быть больше текущей и меньше 1900 года.'


# JWT token
class TokenExpiredException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен истёк'

class TokenAbsentException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен отсутствует'

class IncorrectTokenException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверный формат токена'

# Артикли
class PostNotFound(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Пост не найден'

class PostNotDeleted(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Этот пост не принадлежит вам, вы не можете его удалить'

class PostYetExisting(BaseException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    detail = 'Невозможно удалить пользователя так как у него есть посты'