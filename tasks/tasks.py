import smtplib

from pydantic import EmailStr

from config.config import settings
from tasks.celery_app import celery

from .email_templates import success_created_user


@celery.task
def send_user_confirmation_message(user: dict, email_to: EmailStr):
    msg_content = success_created_user(user, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
