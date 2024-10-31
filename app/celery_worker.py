import os

from celery import Celery
from celery.schedules import crontab

# default url value
_REDIS_URL = "redis://redis/0"
celery_app = Celery(
    'background_tasks', 
    broker=os.getenv("CELERY_BROKER_URL", _REDIS_URL),
    backend=os.getenv("CELERY_BROKER_BACKEND", _REDIS_URL)
)

# celery_app.conf.update(
#     result_expires=3600,
# )
# celery_app.conf.beat_schedule = {
#     'send-email-every-5-minutes': {
#         'task': 'app.tasks.send_email',
#         'schedule': crontab(minute='*/1'),  # Every 5 minutes
#         'args': ('email@dominio.com', "mensaje de prueba")
#     }
# }
