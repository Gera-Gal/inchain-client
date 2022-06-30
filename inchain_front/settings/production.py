from .base import *

import dj_database_url
from decouple import config

SECRET_KEY = config('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default=['inchain-server.herokuapp.com'])

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware', ]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATICFILE_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

#Admin

ADMIN_URL = config('DJANGO_ADMIN_URL')