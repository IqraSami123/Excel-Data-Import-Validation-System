from celery import Celery

celery_app = Celery(
    "excel_import",
    broker="redis://localhost:6379/0",   # redis://localhost:6379/0 is the default Redis URL for Celery broker
    backend="redis://localhost:6379/1",   # redis://localhost:6379/1 is the default Redis URL for Celery result backend
    include=["app.tasks.import_tasks"],
)

celery_app.conf.update(
    timezone="Asia/Karachi",
    enable_utc=True,    # this means that the Celery worker will use UTC time for scheduling tasks, regardless of the local timezone of the machine it's running on.
    task_track_started=True,   # this means that the Celery worker will track when a task has started, which can be useful for monitoring and debugging purposes.
)