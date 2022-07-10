import os
import time
from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="email_sender")
def email_sender(user_verification_url, user_email):
    from src.apis.v1.utils.user_utils import send_email
    return send_email(url=user_verification_url,recipient=user_email)