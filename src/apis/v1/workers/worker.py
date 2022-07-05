import os
import time

from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def create_task(encrypted_user_id):
    #email sender task here, delay of 20 seconds just to test.
    print("email sender task here, delay of 20 seconds just to test.")
    time.sleep(20)
    return True