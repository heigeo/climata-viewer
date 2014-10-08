"""
Django settings for climata_viewer project.
Based on the Django 1.6 template, with wq-specific modifications noted as such

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/

For more information about wq.db's Django settings see
http://wq.io/docs/settings

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
# wq: extra dirname() to account for db/ folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# wq: SECRET_KEY, DEBUG and TEMPLATE_DEBUG are defined in local_settings.py

# climata: ALLOWED_HOSTS is defined in local_settings.py


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'social.apps.django_app.default',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',

    'south',
    'rest_framework',

    'wq.db.patterns.identify',
    'wq.db.patterns.annotate',
    'wq.db.patterns.relate',
    'wq.db.rest.auth',
    'wq.db.contrib.vera',
    'wq.db.contrib.files',
    'wq.db.contrib.dbio',

    'locations',
    'data',
)

MIDDLEWARE_CLASSES = (
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# wq: Recommended settings for Django, rest_framework, and social auth
from wq.db.rest.settings import (
    TEMPLATE_LOADERS,
    TEMPLATE_CONTEXT_PROCESSORS,
    SESSION_COOKIE_HTTPONLY,
    REST_FRAMEWORK,
    SOCIAL_AUTH_PIPELINE,
)
TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',

    'wq.db.rest.auth.context_processors.is_authenticated',
    'wq.db.rest.auth.context_processors.social_auth',
    'wq.db.rest.auth.context_processors.csrftoken',
    'wq.db.rest.context_processors.version',
    'data.context_processors.climata_version',
]

# wq: Recommended settings unique to wq.db
from wq.db.rest.settings import (
    ANONYMOUS_PERMISSIONS,
    SRID,
    DEFAULT_AUTH_GROUP,
    DISAMBIGUATE
)

WQ_SITE_MODEL = "locations.Site"
WQ_EVENT_MODEL = "data.Event"
WQ_EVENTRESULT_MODEL = "data.EventResult"
WQ_DEFAULT_REPORT_STATUS = 1

# wq: Social auth (see http://psa.matiasaguirre.net/docs/backends/)
AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.github.GithubOAuth2',
    'social.backends.linkedin.LinkedinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_REDIRECT_URL = "/"
LOGIN_ERROR_URL = "/"

ROOT_URLCONF = 'climata_viewer.urls'

WSGI_APPLICATION = 'climata_viewer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# wq: DATABASES is defined in local_settings.py

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# wq: Configure paths for default project layout
STATIC_ROOT = os.path.join(BASE_DIR, 'htdocs', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
VERSION_TXT = os.path.join(BASE_DIR, 'version.txt')
MEDIA_URL = '/media/'
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# wq: Import local settings
try:
    from .local_settings import *
except ImportError:
    pass

CELERY_RESULT_BACKEND = BROKER_URL = 'redis://localhost:6379/%s' % REDIS_DB
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'OPTIONS': {
            'DB': REDIS_DB,
        }
    }
}
