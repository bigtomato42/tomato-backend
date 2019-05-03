import os
import django_heroku

from .base import *
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


SECRET_KEY = os.getenv('SECRET_KEY', 'Optional default value')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

WSGI_APPLICATION = 'conf.wsgi.application'



STATIC_URL = '/static/'


django_heroku.settings(locals())
