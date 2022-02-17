"""
Django settings for massenergize_portal_backend project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
from pathlib import Path  # python3 only
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ********  LOAD CONFIG DATA ***********#
# DJANGO_ENV can be passed in through the makefile, with "make start env=local"
DJANGO_ENV = os.environ.get("DJANGO_ENV","remote")
RUN_SERVER_LOCALLY = False
if DJANGO_ENV == "local":
    RUN_SERVER_LOCALLY = True

# Database selection, development DB unless one of these chosen
IS_PROD = False
IS_CANARY = False
IS_LOCAL = False

try:
    if IS_PROD:
        env_path = Path('.') / 'prod.env'
    elif IS_CANARY:
        env_path = Path('.') / 'canary.env'
    elif IS_LOCAL:
        env_path = Path('.') / 'local.env'
    else:
        env_path = Path('.') / 'dev.env'

    load_dotenv(dotenv_path=env_path, verbose=True)

except Exception:
    load_dotenv()


# ********  END LOAD CONFIG DATA ***********#

SECRET_KEY =  os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = RUN_SERVER_LOCALLY

ALLOWED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1',
    'localhost:3000',
    'localhost',
    '.massenergize.org',
    '.massenergize.com',
    '.massenergize.dev',
    '.massenergize.test',
    'MassenergizeApi-env.eba-zfppgz2y.us-east-2.elasticbeanstalk.com',
    'ApiDev-env.eba-5fq2r9ph.us-east-2.elasticbeanstalk.com',
    'dev-api-env.eba-nfqpwkju.us-east-2.elasticbeanstalk.com',
    'massenergize-canary-api.us-east-2.elasticbeanstalk.com',
    'massenergize.test',
    'massenergize.test:3000'
]

if RUN_SERVER_LOCALLY:
    ALLOWED_HOSTS = ['*']
    

INSTALLED_APPS = [
    'django_hosts',
    'authentication',
    'carbon_calculator',
    'database',
    'api',
    'website',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'authentication.middleware.RemoveHeaders',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #custom middlewares
    'authentication.middleware.MassenergizeJWTAuthMiddleware',

    'django_hosts.middleware.HostsResponseMiddleware'
]


#-------- FILE STORAGE CONFIGURATION ---------------------#
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE  = 'storages.backends.s3boto3.S3Boto3Storage'
#-------- FILE STORAGE CONFIGURATION ---------------------#


#-------- AWS CONFIGURATION ---------------------#
AWS_ACCESS_KEY_ID        = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY    = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME  = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_VERSION = os.environ.get('AWS_S3_SIGNATURE_VERSION')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_DEFAULT_ACL  = None
AWS_QUERYSTRING_AUTH = False

#-------- OTHER CONFIGURATION ---------------------#
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
USE_X_FORWARDED_HOST = True
WSGI_APPLICATION = '_main_.wsgi.application'
X_FRAME_OPTIONS = 'SAMEORIGIN'

CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = not DEBUG
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_DEFAULT_ACL = None
APPEND_SLASH = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440*3

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




# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE'   : os.environ.get('DATABASE_ENGINE'),
        'NAME'     : os.environ.get('DATABASE_NAME'),
        'USER'     : os.environ.get('DATABASE_USER'),
        'PASSWORD' : os.environ.get('DATABASE_PASSWORD'),
        'HOST'     : os.environ.get('DATABASE_HOST'),
        'PORT'     : os.environ.get('DATABASE_PORT')
    },
}


# CACHES = {
#     'default': {
#         'BACKEND': os.getenv('CACHE_BACKEND'),
#         'LOCATION': os.getenv('CACHE_LOCATION'),
#     }
# }

# url and hosts config
ROOT_URLCONF = '_main_.urls'
ROOT_HOSTCONF = '_main_.hosts'
DEFAULT_HOST = 'main'


# firebase setup
FIREBASE_CREDENTIALS = credentials.Certificate({
  "type": "service_account",
  "project_id": os.environ.get('FIREBASE_SERVICE_ACCOUNT_PROJECT_ID'),
  "private_key_id": os.environ.get('FIREBASE_SERVICE_ACCOUNT_PRIVATE_KEY_ID'),
  "private_key": os.environ.get('FIREBASE_SERVICE_ACCOUNT_PRIVATE_KEY'),
  "client_email": os.environ.get('FIREBASE_SERVICE_ACCOUNT_CLIENT_EMAIL'),
  "client_id": os.environ.get('FIREBASE_SERVICE_ACCOUNT_CLIENT_ID'),
  "client_x509_cert_url": os.environ.get('FIREBASE_SERVICE_ACCOUNT_CLIENT_URL'),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
})
firebase_admin.initialize_app(FIREBASE_CREDENTIALS)


# Password validation
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


# Sentry Logging Initialization
sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
EMAIL_USE_TLS = True 
EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_PORT = 587 
EMAIL_HOST_USER = os.environ.get('EMAIL')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_POSTMARK_SERVER_TOKEN = os.environ.get('EMAIL_POSTMARK_SERVER_TOKEN')


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Simplified static file serving.
STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

