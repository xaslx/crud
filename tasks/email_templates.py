from email.message import EmailMessage
from pydantic import EmailStr
from config.config import settings



def success_created_user(username: str, email_to: EmailStr, token: str):
    email = EmailMessage()
    email["Subject"] = "Успешная регистрация"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <h2>Спасибо за регистрацию на нашем сервисе</h2>
        <p>Ваш логин: {username}</p>

        <p>Нажмитие на кнопку ниже для верификации вашего аккаунта</p>
        <br>
        <a style=" padding: 1rem; width: 250px; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #0275d8; color: white;" href="http://127.0.0.1:8000/auth/verification/?token={token}">
            Пройти верификацию
        <a>
        <br>
        <br>
        <p>Если вы не регистрировались на нашем сервисе, то проигнорируйте данное письмо</p>
    """,
        subtype="html",
    )

    return email


def forgot_password_email(email_to: EmailStr, token: str):
    email = EmailMessage()
    email["Subject"] = "Сброс пароля"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <h2>Вы сделали запрос на сброс пароля</h2>

        <p>Нажмитие на кнопку ниже для сброса вашего пароля</p>
        <br>
        <a style=" padding: 1rem; width: 250px; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #0275d8; color: white;" href="http://127.0.0.1:8000/auth/reset_password/?token={token}">
            Сбросить пароль
        <a>
        <br>
        <br>
        <p>Если вы ничего не запрашивали, то проигнорируйте данное письмо</p>
    """,
        subtype="html",
    )

    return email


def password_changed_email(email_to: EmailStr, username: str, new_password: str):
    email = EmailMessage()
    email["Subject"] = "Пароль изменен"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(f"""
        <h3>Ваш пароль был сброшен</h3>
        <b><p>Ваш логин: {username}</p></b>
        <b><p>Новый пароль: {new_password}</p></b>
        <b><p>Теперь вы можете войти в систему с новым паролем и изменить его если захотите</p></b>
    """, 
    subtype='html',
    )

    return email