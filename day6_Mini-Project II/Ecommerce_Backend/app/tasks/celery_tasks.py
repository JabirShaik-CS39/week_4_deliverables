from app.core.celery_app import celery_app
from celery.exceptions import Retry
import random

@celery_app.task
def send_welcome_email(email: str):
    print(f"Sending welcome email to {email}")

    return {
        "status": "success",
        "email": email
    }


@celery_app.task
def generate_report():
    print("Generating report...")

    return {
        "status": "success"
    }


@celery_app.task
def process_image(image_name: str):
    print(f"Processing {image_name}")

    return {
        "status": "success",
        "image": image_name
    }


# =====================================
# RETRY TASK
# =====================================
@celery_app.task(
    bind=True,
    max_retries=3
)
def unstable_task(self):

    try:

        if random.randint(1, 3) != 1:
            raise Exception("Temporary failure")

        return {
            "status": "success"
        }

    except Exception as exc:

        countdown = 2 ** self.request.retries

        raise self.retry(
            exc=exc,
            countdown=countdown
        )
    
@celery_app.task
def scheduled_report():

    print("Generating daily report...")

    return {
        "status": "report generated"
    }