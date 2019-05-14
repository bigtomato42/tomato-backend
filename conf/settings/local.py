import os
import django_heroku
from .base import *
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


SECRET_KEY = 'nvk3(06snl(z=6xw6--)4%3l=%4jpptiiy006&zf$%j73waqhi'

DEBUG = True
ALLOWED_HOSTS = ['*']



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '..', 'static'),
)

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'development_db',
        'USER': 'development',
        'PASSWORD': 'development',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}




STATIC_URL = '/static/'
