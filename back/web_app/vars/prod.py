from .drf import * # noqa

DEBUG = False

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', [])

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', [])

DATABASES = {
    'default': {
        'ENGINE': env.str('DB_ENGINE'),
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.str('DB_PORT'),
    }
}

MEDIA_ROOT = env.str('MEDIA_ROOT')
