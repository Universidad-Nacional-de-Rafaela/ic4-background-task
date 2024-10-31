import logging

from celery.result import AsyncResult
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from celery_tasks import send_email, add_numbers
from celery_worker import celery_app


app = FastAPI()

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    filename="logs/app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class EmailMessage(BaseModel):
    email: str
    msg: str


@app.post("/send-email")
def send_email_view(request: EmailMessage):
    task = send_email.delay(request.email, request.msg)
    return {"task_id": task.id}


@app.post("/add-numbers", status_code=202)
def add_numbers_view(payload = Body(...)):
    a = payload.get("a", 100)
    b = payload.get("b", 100)
    task = add_numbers.delay(a, b)
    return {"task_id": task.id}


@app.get("/status/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id, app=celery_app)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return JSONResponse(result)
