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

