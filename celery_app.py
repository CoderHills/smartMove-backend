from celery import Celery

# Get Flask app factory
from app import create_app

def make_celery(app):
    """Create Celery instance using Flask app config."""
    celery = Celery(
        app.import_name,
        broker=app.config.get('CELERY_BROKER_URL'),
        backend=app.config.get('CELERY_RESULT_BACKEND')
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

flask_app = create_app()
celery_app = make_celery(flask_app)
