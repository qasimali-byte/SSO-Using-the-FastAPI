"""prefork worker doesn't work in windows , so we have to use (-P solo) or (-P eventlet)\
as following:
celery -A worker worker --loglevel=INFO -P eventlet
"""
import os
from dotenv import load_dotenv
from utility import send_email
from celery import Celery
celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://18.134.217.103:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://18.134.217.103:6379")
load_dotenv(dotenv_path=".env.worker")


@celery.task(name="email_sender")
def email_sender(user_verification_url, user_email):
    return send_email(url=user_verification_url,recipient=user_email)