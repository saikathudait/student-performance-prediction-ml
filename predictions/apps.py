import sys

from django.apps import AppConfig
from django.conf import settings


class PredictionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "predictions"

    def ready(self):
        should_load = settings.LOAD_MODEL_ON_STARTUP and any(
            cmd in sys.argv for cmd in ["runserver", "gunicorn", "uwsgi", "daphne"]
        )
        if should_load:
            from .services import load_model

            load_model()
