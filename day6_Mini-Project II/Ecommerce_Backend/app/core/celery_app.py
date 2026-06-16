from celery import Celery

celery_app = Celery(
    "ecommerce",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.autodiscover_tasks([
    "app.tasks"
])


celery_app.conf.beat_schedule = {
    "generate-report-every-minute": {

        "task":
        "app.tasks.celery_tasks.scheduled_report",

        "schedule":
        60.0
    }
}

celery_app.conf.timezone = "UTC"