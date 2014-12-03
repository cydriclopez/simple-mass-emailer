"""
Django settings for myproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import local_settings
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = local_settings.SECRET_KEY

TESTING = ("test" in sys.argv)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_mass_emailer',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'myproject.urls'
WSGI_APPLICATION = 'myproject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbmain1',
        'USER': local_settings.DB_USER,
        'PASSWORD': local_settings.DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True

# USE_TZ = False is needed to prevent conflict with "non-naive dates" in postgresql.
# USE_TZ = True
USE_TZ = False

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_DOMAIN = None

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/user1/Projects/simple-mass-emailer/simple-mass-emailer/myproject/simple_mass_emailer'
STATICFILES_DIRS = (
    '/home/user1/Projects/simple-mass-emailer/simple-mass-emailer/myproject/simple_mass_emailer/static',
)
TEMPLATE_DIRS = (
    '/home/user1/Projects/simple-mass-emailer/simple-mass-emailer/myproject/simple_mass_emailer/template',
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
EMAIL_PORT = 25
EMAIL_HOST = local_settings.EMAIL_HOST
EMAIL_HOST_USER = local_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = local_settings.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = local_settings.DEFAULT_FROM_EMAIL
SERVER_EMAIL = local_settings.SERVER_EMAIL
