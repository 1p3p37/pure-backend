# flake8: noqa
"""
Local Django settings for Backend project.
"""
from datetime import timedelta

from celery.schedules import crontab

from .base import *


# Временный секретный ключ на период разработки
SECRET_KEY: str = environ.get('BACKEND_SECRET_KEY')

ALLOWED_HOSTS: list = []

# Настройки django_debug_tools
INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS: list = [
    '127.0.0.1',
    '0.0.0.0',
]
