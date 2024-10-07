import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1","*", "141.8.193.4", "sferamsk.fun"]

SECRET_KEY = 'django-insecure-oz#3z7@s@kqjr4=y3)_j7w3x@bj_ypmb^ek4-3fb0tkhaie#l='

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sphera',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',

    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')#путь к общей папке статик в которую собираются все файлы статик в режиме дебаг фолс
STATICFILES_DIRS=[STATIC_DIR]#список нестандартных путей
