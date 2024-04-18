import smtplib

from pydantic import EmailStr

from config.config import settings
from tasks.celery_app import celery

from .email_templates import success_created_user
from PIL import Image

@celery.task
def send_user_confirmation_message(
    username: str, email_to: EmailStr, token: str
):
    msg_content = success_created_user(username, email_to, token)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)

@celery.task
def save_image(name: str):
    img = Image.open(name)
    img = img.resize(size=(200, 200))
    img.save(name)
