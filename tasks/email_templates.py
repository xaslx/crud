from email.message import EmailMessage

from pydantic import EmailStr

from config.config import settings


def success_created_user(user: dict, email_to: EmailStr):
    email = EmailMessage()

    email["Subject"] = "Успешная регистрация"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Вы зарегистрировались</h1>
            <h3>Ваш логин: {user}</h3>
        """,
        subtype="html",
    )

    return email
