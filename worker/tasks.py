import os
from time import sleep
import traceback

from celery import Celery
from celery import states


CELERY_BROKER_URL = os.getenv("REDISSERVER", "redis://redis_server:6379")
CELERY_RESULT_BACKEND = os.getenv("REDISSERVER", "redis://redis_server:6379")


celery = Celery(
    "celery", backend=CELERY_BROKER_URL, broker=CELERY_RESULT_BACKEND
)


@celery.task(name='run_ai_algorithm', bind=True)
def run_ai_algorithm(self, class_to_select):
    for i in range(20):
        self.update_state(state='PROGRESS', meta={'done': i, 'total': 20})
        sleep(1)
    prediction = [0, 0, 0, 0, 0]
    prediction[class_to_select] = 1
    return {"prediction": prediction, 'done': 20, 'total': 20}
    