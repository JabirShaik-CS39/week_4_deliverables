from app.tasks.celery_tasks import send_welcome_email

result = send_welcome_email.delay("test@gmail.com")

print(result.id)