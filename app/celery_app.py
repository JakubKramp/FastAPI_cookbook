from celery import Celery

from config import settings

celery_app = Celery(broker=settings.CELERY_BROKER_URL, include=["fridge.tasks"])


celery_app.conf.beat_schedule = {
    "mark-expired-products": {
        "task": "fridge.tasks.mark_expired_products",
        "schedule": 30.0,
    },
}
celery_app.conf.timezone = "UTC"
