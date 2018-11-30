# tasks.py
# pylint: disable=missing-docstring

# Run with:
#    pipenv run celery -A tasks.celery worker --loglevel=INFO --pool=solo


from celery import Celery
from wsgi import application

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(application)

@celery.task()
def very_slow_add(a, b):
    import time
    time.sleep(3)
    return a + b
