import logging
import os

from celery import Celery
from celery.signals import setup_logging
from django.conf import settings
from django_structlog.celery.steps import DjangoStructLogInitStep

from .settings import configure_structlog

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bittensor_panel.settings")

app = Celery("bittensor_panel")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.steps["worker"].add(DjangoStructLogInitStep)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@setup_logging.connect
def receiver_setup_logging(loglevel, logfile, format, colorize, **kwargs):  # pragma: no cover
    logging.config.dictConfig(settings.LOGGING)
    configure_structlog()


def route_task(name, args, kwargs, options, task=None, **kw):
    return {"queue": "celery"}
