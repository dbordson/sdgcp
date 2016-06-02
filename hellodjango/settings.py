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

# for gmail or google apps
try:
    from emailpw import SD_EMAIL_PW
except:
    SD_EMAIL_PW = os.environ['SD_EMAIL_PW']
    GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sadaalpha@gmail.com'
EMAIL_HOST_PASSWORD = SD_EMAIL_PW
EMAIL_PORT = 587

LOGIN_URL = '/accounts/login/'

PROJECT_ID = 'sdapp-1305'
CLOUD_STORAGE_BUCKET = 'indexbucket'

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
    'django.contrib.humanize',
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
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'hellodjango.urls'

WSGI_APPLICATION = 'hellodjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/sdapp-1305:us-east1:sd',
            'NAME': 'sd',
            'USER': 'root',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'sd',
            'USER': 'root',
            'PASSWORD': 'coconut257',
            'HOST': '104.196.140.6',
            'PORT': '3306',
        }
    }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'sd',
#         'USER': 'root',
#         'PASSWORD': 'coconut257',
#         'HOST': '104.196.140.6',
#         'PORT': '3306',
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

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

# STATIC_URL = '/static/'
STATIC_URL = 'http://storage.googleapis.com/sdapp-1305-static/static/'

STATIC_ROOT = 'static/'

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )
# STATICFILES_DIRS = (
#     'http://storage.googleapis.com/sdapp-1305-static/static/',
# )

# if DEBUG:
#     MEDIA_URL = '/media/'
#     STATIC_ROOT =\
#         os.path.join(os.path.dirname(BASE_DIR), "static", "static-only")
#     MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "media")
#     STATICFILES_DIRS = (
#         os.path.join(os.path.dirname(BASE_DIR), "static", "static"),
#     )
