import os
from .base import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


SECRET_KEY = 'nvk3(06snl(z=6xw6--)4%3l=%4jpptiiy006&zf$%j73waqhi'

DEBUG = True
ALLOWED_HOSTS = ['*']


STATIC_ROOT = os.path.join(BASE_DIR, '..', 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '..', 'static'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'circle_test',
        'USER': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


STATIC_URL = '/static/'
