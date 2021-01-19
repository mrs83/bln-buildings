from celery import Celery

from app.core.config import CELERY_BROKER_URL


celery_app = Celery("worker", broker=CELERY_BROKER_URL)
celery_app.conf.task_routes = {"app.tasks.*": "main-queue"}
