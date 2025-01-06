# auto_wage_schedule/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auto_wage_schedule.settings")
app = Celery("auto_wage_schedule")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
