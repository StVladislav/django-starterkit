from dotenv import load_dotenv
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+k$@++jjvvfv6qjxfc12uar=kim$26g=z$4(&k=9n=2&ykuff*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG and not os.environ.get("IS_DOCKER", None):
    load_dotenv("deploy/localhost.dev.env")

ALLOWED_HOSTS = ['127.0.0.1', 'localhost'] # Use your ip addres or domain

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# Application definition
INSTALLED_APPS = [
    # System apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Package apps
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders',
    'django_resized',
    'django_celery_beat', # use this if you want to run celery periodic tasks from database (e.g. manage from django-admin)
    # Project apps
    'src.authentication',
    'src.examples', # you can disable this app for a production
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
TIME_ZONE = 'Europe/Minsk'

# Database default SQLite
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Database PostgreSQL. For high load app use django-db-geventpool
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'connect_timeout': 10000,  # Time in seconds to wait for a connection
            'options': '-c statement_timeout=300000', # Time query handling in ms
            'options': '-c search_path=public', # Set schema. By default public for test. In production use another schema
        },
        'NAME': os.environ.get('DATABASE_NAME', 'test_db'),
        'USER': os.environ.get('DATABASE_USER' ,'admin'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD' ,'123'),
        'HOST': os.environ.get('DATABASE_HOST' ,'postgres'),
        'PORT': os.environ.get('DATABASE_PORT', '5432')
    }
}

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # DRF token authentication
        # 'rest_framework_simplejwt.authentication.JWTAuthentication', # JWT token authentication
    ],
}

# DJOSER
DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,  # Require repeating password
    'SERIALIZERS': {
        'user_create_password_retype': 'src.authentication.serializers.CustomUserCreateSerializer',
    },
}

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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTHETICATION MODEL
AUTH_USER_MODEL = 'authentication.User'

MEDIA_URL = '/media/' # Default media url
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STORAGE_BUCKET_NAME}/' # Using with S3

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CONFIG FOR RESIZING IMAGES (ResizedFields use from utils.fields)
DJANGORESIZED_DEFAULT_UPLOAD_TO = 'images'
DJANGORESIZED_DEFAULT_SIZE = [1024, 768] # set approximate size
DJANGORESIZED_DEFAULT_QUALITY = 80 # pct of an initial image quality 
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = False # This setting does not work with Apple iPhone images. Rotate images mannualy or using javascript
DJANGORESIZED_DEFAULT_KEEP_META = False # Delete any meta data
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'WEBP'

# Celery settings using Redis
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", 'redis://localhost:6379/0') # Using Redis with database for tasks - 0
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1') # Using Redis with database for results - 1
CELERY_ACCEPT_CONTENT = ['json'] # dont use pickle
CELERY_TASK_SERIALIZER = 'json' # dont use pickle
CELERY_RESULT_SERIALIZER = 'json' # dont use pickle
CELERY_TIMEZONE = TIME_ZONE # This should be equal
CELERY_RESULT_EXPIRES = 86400  # 24 hours TTL (time to live) for tasks result in the redis database
CELERY_TASK_TRACK_STARTED = True  # Save task start time
CELERY_TASK_ACKS_LATE = True # Should celery rerun failed task
CELERY_TASK_RETRY_DELAY = 30  # Timeout between trying task in secs

# Celery-beat settings using database scheduler. Use this pnly with PostgreSQL
# After migrate open django-admin and manage each shared_task
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Email settigns. Example for a gmail account
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "youremail@gmail.com")  # Your email address
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "app pass")  # App password. You can create it here https://myaccount.google.com/apppasswords
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "youremail@gmail.com")  # Sender email address

# S3 STORAGE CREDENTIALS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_STORAGE_PROTECTED_BUCKET_NAME = os.environ.get('AWS_STORAGE_PROTECTED_BUCKET_NAME', '')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', '')
AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL', '')
AWS_S3_ADDRESSING_STYLE = os.environ.get('AWS_S3_ADDRESSING_STYLE', '')
AWS_S3_SIGNATURE_VERSION = os.environ.get('AWS_S3_SIGNATURE_VERSION', '')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN', '')

# SET LOGGING FOR PRODUCTION ON A SERVER
if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {funcName}:{lineno} {message}',
                'style': '{',
            }
        },
        'handlers': {
            'gunicorn_file': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '/var/log/gunicorn.log', # Change path for log file. Check permissions on the server
                'maxBytes': 5*1024*1024, # In bytes 
                'backupCount': 0, # Without backups
                'formatter': 'verbose'
            },
        },
        'loggers': {
            '': {
                'handlers': ['gunicorn_file',],
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }