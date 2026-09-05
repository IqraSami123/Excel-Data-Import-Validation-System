from app.celery_app import celery_app


@celery_app.task
def test_celery_task():
    ### just to test if celery is working or not"""
    return "Celery is working!"