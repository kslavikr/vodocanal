"""
Django settings for countersweb project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.dirname(BASE_DIR)+"/configuration.json") as data_file:
    data = json.load(data_file)
    #print(data["main_db"])

if data:
    user_main_db = data["main_db"]["user_main_db"]
    passw_main_db = data["main_db"]["passw_main_db"]
    host_main_db = data["main_db"]["host_main_db"]
    name_main_db = data["main_db"]["name_main_db"]

    user_sync_db = data["sync_db"]["user_sync_db"]
    passw_sync_db = data["sync_db"]["passw_sync_db"]
    host_sync_db = data["sync_db"]["host_sync_db"]
    name_sync_db = data["sync_db"]["name_sync_db"]
    host_url = data["url_for_login"]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SECRET_KEY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'countersweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'countersweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': name_main_db,
        'USER': user_main_db,
        'PASSWORD': passw_main_db,
        'HOST': host_main_db,
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
PROJECT_DIR  = (os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

EMAIL_HOST = data["mail_conf"]["EMAIL_HOST"]
EMAIL_HOST_USER =  data["mail_conf"]["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD =  data["mail_conf"]["EMAIL_HOST_PASSWORD"]
EMAIL_PORT = 465
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL =  data["mail_conf"]["DEFAULT_FROM_EMAIL"]

SESSION_COOKIE_AGE = 1800
