# app/celery_app.py
from celery import Celery


def create_celery(app=None):
    celery = Celery(
        app.import_name if app else __name__,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )

    class AppContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = AppContextTask
    if app:
        celery.conf.update(app.config)
    celery.autodiscover_tasks(['app.services'])  # Add this line
    return celery