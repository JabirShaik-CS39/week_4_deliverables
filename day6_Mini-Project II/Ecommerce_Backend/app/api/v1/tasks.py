from fastapi import APIRouter

from celery.result import AsyncResult
from app.tasks.celery_tasks import unstable_task
from app.core.celery_app import celery_app
from app.tasks.celery_tasks import send_welcome_email

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/send-email")
async def send_email(email: str):

    task = send_welcome_email.delay(email)

    return {
        "task_id": task.id,
        "status": "submitted"
    }


@router.get("/{task_id}")
async def get_task_status(task_id: str):

    task = AsyncResult(
        task_id,
        app=celery_app
    )

    return {
        "task_id": task.id,
        "state": task.state,
        "result": task.result
    }

@router.post("/retry-test")
async def retry_test():

    task = unstable_task.delay()

    return {
        "task_id": task.id
    }