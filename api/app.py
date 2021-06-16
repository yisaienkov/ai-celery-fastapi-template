import os
from typing import List, Optional

from pydantic import BaseModel
from fastapi import FastAPI
from celery import Celery
from pydantic.types import NoneBytes


CELERY_BROKER_URL = os.getenv("REDISSERVER")
CELERY_RESULT_BACKEND = os.getenv("REDISSERVER")


celery = Celery(
    "celery", backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URL
)
app = FastAPI()


class InputData(BaseModel):
    class_to_select: int


class TaskMeta(BaseModel):
    id: str
    url: str


class AlgorithmOutput(BaseModel):
    prediction: Optional[List[float]]


class ProcessMeta(BaseModel):
    percent: float


class TaskResult(BaseModel):
    status: str
    result: AlgorithmOutput
    task_id: str
    info: ProcessMeta


@app.get(f"/health")
def health():
    return 200


@app.post("/task", response_model=TaskMeta)
def create_task(input_data: InputData):
    task_name = "run_ai_algorithm"
    task = celery.send_task(task_name, args=[input_data.class_to_select])

    return TaskMeta(id=task.id, url=f"/task/{task.id}")


@app.get("/task/{task_id}", response_model=TaskResult)
def check_task(task_id: str):
    task = celery.AsyncResult(task_id)

    response = TaskResult(
        status=task.status,
        result=AlgorithmOutput(prediction=task.info.get("prediction", None)),
        task_id=task_id,
        info=ProcessMeta(percent=task.info["done"] / task.info["total"]),
    )

    return response