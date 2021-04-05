from flask import Flask, request, jsonify
from celery.result import AsyncResult

from tasks import celery as app_celery, create_task


app = Flask(__name__)


@app.route("/tasks", methods=["GET"])
def run_task():
    task_type = int(request.args.get("task_type", 0))
    task = create_task.delay(int(task_type))

    return jsonify({"task_id": task.id}), 202


@app.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    task_result = AsyncResult(task_id, app=app_celery)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return jsonify(result), 200