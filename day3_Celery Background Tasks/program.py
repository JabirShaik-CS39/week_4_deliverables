## 4. Configure Celery
# celery_app.py

from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_track_started=True
)


## 5. Create Tasks
# tasks.py
from celery import Celery
from celery_app import celery_app
import time

@celery_app.task
def send_welcome_email(email):
    time.sleep(5)

    return f"Email sent to {email}"

## Basic Retry
@celery_app.task(bind=True)
def send_email(self):

    try:
        raise Exception()

    except Exception as exc:
        raise self.retry(
            exc=exc,
            countdown=10
        )
        
## Example
@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5}
)
def process_ai(self):
    pass



## FastAPI BackgroundTasks

from fastapi import BackgroundTasks

@app.post("/send")
async def send_email(
    background_tasks: BackgroundTasks
):

    background_tasks.add_task(
        send_email
    )

    return {"message": "started"}
