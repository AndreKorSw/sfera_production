import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-oz#3z7@s@kqjr4=y3)_j7w3x@bj_ypmb^ek4-3fb0tkhaie#l='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1",]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS=[STATIC_DIR]#список нестандартных путей
