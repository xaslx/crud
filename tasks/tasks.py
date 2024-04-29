import smtplib
from smtplib import SMTPResponseException

from PIL import Image
from pydantic import EmailStr

from config.config import settings
from logger import logger
from tasks.celery_app import celery

from .email_templates import (
    forgot_password_email,
    password_changed_email,
    success_created_user,
)


@celery.task
def send_user_confirmation_message(
    username: str, email_to: EmailStr, token: str
):
    msg_content = success_created_user(username, email_to, token)
    try:
        with smtplib.SMTP_SSL(
            settings.SMTP_HOST, settings.SMTP_PORT
        ) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg_content)
    except SMTPResponseException:
        logger.error(
            "Произошла ошибка при отправке письма на почту",
            exc_info={
                "data": [username, email_to, msg_content],
                "token": token,
            },
        )
        return None


@celery.task
def reset_password_email(email: EmailStr, token: str):
    msg_content = forgot_password_email(email, token)

    try:
        with smtplib.SMTP_SSL(
            settings.SMTP_HOST, settings.SMTP_PORT
        ) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg_content)
    except SMTPResponseException:
        logger.error(
            "Произошла ошибка при отправке письма на почту",
            exc_info={"data": email, "token": token},
        )
        return None


@celery.task
def password_changed(email: EmailStr, username: str, new_password: str):

    msg_content = password_changed_email(email, username, new_password)

    try:
        with smtplib.SMTP_SSL(
            settings.SMTP_HOST, settings.SMTP_PORT
        ) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg_content)
    except SMTPResponseException:
        logger.error(
            "Произошла ошибка при отправке письма на почту",
            exc_info={"data": [username, email, msg_content, new_password]},
        )
        return None


@celery.task
def save_image(name: str):
    img = Image.open(name)
    img = img.resize(size=(200, 200))
    img.save(name)
