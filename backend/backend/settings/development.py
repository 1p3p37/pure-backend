# flake8: noqa
"""
Development Django settings for Backend project.
"""
from datetime import timedelta

from celery.schedules import crontab

from corsheaders.defaults import default_headers

from .base import *


SECRET_KEY: str = environ.get('BACKEND_SECRET_KEY')

ALLOWED_HOSTS: list = ['*', ]

SESSION_COOKIE_SAMESITE: str = 'None'
SESSION_COOKIE_SECURE: bool = True

CSRF_COOKIE_SAMESITE: str = 'None'
CSRF_COOKIE_SECURE: bool = True

SESSION_COOKIE_DOMAIN: str = ORIGIN_DOMAIN
CSRF_COOKIE_DOMAIN: str = ORIGIN_DOMAIN

CSRF_TRUSTED_ORIGINS: list = environ.get('CSRF_TRUSTED_ORIGINS').split()

SECURE_PROXY_SSL_HEADER: tuple = (
    'HTTP_X_FORWARDED_PROTO',
    'https',
)
SECURE_SSL_REDIRECT: bool = True

# DCH settings
CORS_ALLOWED_ORIGINS: list = environ.get('CORS_ALLOWED_ORIGINS').split()
CORS_ORIGIN_WHITELIST: list = CORS_ALLOWED_ORIGINS
CORS_ALLOW_CREDENTIALS: bool = True
CORS_ALLOW_HEADERS: list = list(default_headers)
CORS_ALLOW_HEADERS.extend(
    [
        'access-control-allow-headers',
        'access-control-allow-credentials',
        'access-control-allow-origin',
        'cache-control',
        'cookie',
        'expires',
        'pragma',
    ]
)
CORS_ORIGIN_ALLOW_ALL = bool(int(environ.get('CORS_ORIGIN_ALLOW_ALL')))
CORS_ALLOW_METHODS: list = environ.get('CORS_ALLOW_METHODS').split()

# CELERY settings


MAX_RESEND_TXN_ATTEMPTS: int = 10