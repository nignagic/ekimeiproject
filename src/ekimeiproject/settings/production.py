# settings/local.py

from .base import *
import environ

env = environ.Env()
env.read_env('.env')

PROJECT_DIR = environ.Path(__file__) - 2
BASE_DIR = environ.Path(__file__) - 3

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG',default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('MYSQL_DATABASE'),
        'USER': env('MYSQL_USER'),
        'PASSWORD': env('MYSQL_PASSWORD'),
        'HOST': 'db',
        'PORT': '3306'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': env('CACHE_TABLE'),
    }
}

# 追加もしくは変更
STATIC_ROOT = BASE_DIR("static")
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR("media")
MEDIA_URL = "/media/"

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True