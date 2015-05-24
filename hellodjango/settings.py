"""
Django settings for hellodjango project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGIN_URL = '/accounts/login/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p#mvoa0nm-xxjm5@3vu8qt_a8c%+5*8l%(v1id-^&cb(_2d_$n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "static", "templates"),
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'signups',
    'south',
    'sdapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hellodjango.urls'

WSGI_APPLICATION = 'hellodjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'da29ata4en7cmb',
        'USER': 'ikgoypfxauimde',
        'PASSWORD': 'qGW1rvAFyqlsJvJvtCrM-YjXNi',
        'HOST': 'ec2-54-243-50-213.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'local sdapp',
#         'USER': 'postgres',
#         'PASSWORD': 'es33-69Cd',
#         'HOST': ''
#     }
# }

# Parse database configuration from $DATABASE_URL

# try:
#     import dj_database_url
#     DATABASES['default'] = dj_database_url.config()
# except:
#     pass

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# if DEBUG:
#     MEDIA_URL = '/media/'
#     STATIC_ROOT =\
#         os.path.join(os.path.dirname(BASE_DIR), "static", "static-only")
#     MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "media")
#     STATICFILES_DIRS = (
#         os.path.join(os.path.dirname(BASE_DIR), "static", "static"),
#     )
