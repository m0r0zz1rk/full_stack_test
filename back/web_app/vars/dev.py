import os
from .drf import * # noqa

DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    'http://*',
    'https://*'
]

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]
