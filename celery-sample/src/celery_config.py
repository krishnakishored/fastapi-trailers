from config import Settings, get_settings

settings: Settings = get_settings()
# celery_app.conf.broker_url = settings.CELERY_BROKER_URL
# celery_app.conf.result_backend = settings.CELERY_RESULT_BACKEND

broker_url = settings.CELERY_BROKER_URL
result_backend = settings.CELERY_RESULT_BACKEND
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
# timezone = "Europe/Oslo" # defaults to UTC
enable_utc = True
include = ["tasks"]
result_expires = 3600
# route a task to a dedicated queue:
task_routes = {
    "tasks.add": "low-priority",
}

# rate limit the task so that only 10 tasks of this type can be processed in a minute (10/m):
task_annotations = {"tasks.add": {"rate_limit": "10/m"}}
