# Django settings for boredshopper project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bshopper',                      # Or path to database file if using sqlite3.
       # The following settings are not used with sqlite3:
        'USER': 'bshopper',
        'PASSWORD': 'pADr4bru',
        'HOST': 'db-sp02.csajctddlmv4.us-east-1.rds.amazonaws.com',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}
#db-sp02.csajctddlmv4.us-east-1.rds.amazonaws.com:3306
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#       'NAME': 'bshopper',                      # Or path to database file if using sqlite3.
#      # The following settings are not used with sqlite3:
#        'USER': 'root',
#        'PASSWORD': 'root',
#        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#        'PORT': '',                      # Set to empty string for default.
#    }
#}
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
DEFAULT_S3_PATH = "media"
STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
STATIC_S3_PATH = "static"
AWS_ACCESS_KEY_ID = "AKIAIFTYD3KFATW7VE6Q"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "static.boredshopper.com"
AWS_S3_SECURE_URLS = False
MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
#MEDIA_URL = '//dvmvdma81sl7r.cloudfront.net/media/'
STATIC_ROOT = "/%s/" % STATIC_S3_PATH
#STATIC_URL = '//dvmvdma81sl7r.cloudfront.net/static/'

MEDIA_URL = '//s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = '//s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
#FACEBOOK_PROFILE_IMAGE_PATH = os.path.join('static/media/images', 'facebook_profiles/%Y/%m/%d')


#MEDIA_URL = '/media/'
#MEDIA_ROOT = ''
#STATIC_ROOT = ''
#STATIC_URL = '/static/'
#static_path = os.path.join(os.path.dirname(__file__), '..', 'static').replace('\\', '/')

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
# MEDIA_ROOT = ''
#MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '..', 'bshopper_app\\static\\media').replace('\\', '/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
#MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
#STATIC_URL = '/static/'

#static_path = os.path.join(os.path.dirname(__file__), '..', 'static').replace('\\', '/')
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#    static_path,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3kb@n#8vz@qm-g+%qolczeaut_38kgzhbwk1+70dj93y))b+-('

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'boredshopper.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'boredshopper.wsgi.application'

import os
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\','/'),)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'bshopper_app',
    'emailconfirmation',
    'django_facebook',
    'south',
    'open_facebook',
    'mailchimp',
    'chimpusers',
    'mailsnake',
    's3_folder_storage',
    'share',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_CONFIRMATION_DAYS = 2
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = "info@boredshopper.com"
EMAIL_HOST = 'in.mailjet.com'
#EMAIL_HOST_USER = 'info@boredshopper.com'
EMAIL_HOST_USER = '97daf1f37f41fc65158622a44113ee7c'
EMAIL_HOST_PASSWORD = '302f27e27f2a6a9c3b07f073a9855715'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
#DEFAULT_FROM_EMAIL = "grytsenko.bamboo@gmail.com"
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = 'grytsenko.bamboo@gmail.com'
#EMAIL_HOST_PASSWORD = 'XXX'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True

#FACEBOOK_APP_ID = '215464901804004'
#FACEBOOK_APP_SECRET = '0aceba27823a9dfefa955f76949fa4b4'
FACEBOOK_APP_ID = '542661562450512'
FACEBOOK_APP_SECRET = '9cf3165a5944cf97fca530a30eb62d1b'


TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django_facebook.context_processors.facebook',
]

AUTHENTICATION_BACKENDS = (
      'django_facebook.auth_backends.FacebookBackend',
      'django.contrib.auth.backends.ModelBackend',
)
AUTH_USER_MODEL = 'django_facebook.FacebookCustomUser'

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
#LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
#LOGIN_URL = '/accounts/signin/'
#LOGOUT_URL = '/accounts/signout/'
#LOGIN_REDIRECT_URL = "/"
FACEBOOK_LOGIN_DEFAULT_REDIRECT = "/"
#LOGIN_URL = '/login/'
#LOGOUT_URL = '/logout/'

MAILCHIMP_API_KEY = "b0252dd4bafe195a8bf96e3a0f9f843b-us2"
MAILCHIMP_LIST_NAME = "Bored Shopper"
MAILCHIMP_LIST_ID = "f533561106"

#AUTH_PROFILE_MODULE = 'django_facebook.FacebookCustomUser'