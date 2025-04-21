import os
import socket
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

DEBUG = os.getenv('DEBUG', False) == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '*']

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())

INTERNAL_IPS = ['127.0.0.1'] + [ip[:-1] + '1' for ip in ips]

DEBUG_TOOLBAR_CONFIG = {
      'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}

CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:8080',]

STATE_FILE_PATH = os.getenv('STATE_FILE_PATH', 'state.json')

ES_HOST = os.getenv('ES_HOST', 'http://elasticsearch:9200')

ES_INDEX_SCHEMA_PATH = os.getenv('ES_INDEX_SCHEMA_PATH', 'movies_index_schema.json')

POLL_INTERVAL = int(os.getenv('POLL_INTERVAL', 10))


# ES_INDEX_NAME = 'movies'

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'movies',
]

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar',]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'example.urls'

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

WSGI_APPLICATION = 'example.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('SQL_HOST', '127.0.0.1'),
        'PORT': os.getenv('SQL_PORT', 5432),
        'OPTIONS': {
            'options': os.getenv('SQL_OPTIONS', '-c search_path=public'),
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'movies.api.v1.renderers.PrettyJSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'movies.api.v1.pagination.FilmWorkPagination',
    'PAGE_SIZE': 50,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        },
    },
    'handlers': {
        'debug-console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['debug-console'],
            'propagate': False,
        }
    },
}

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

LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATIC_ROOT = '/opt/app/static'

MEDIA_ROOT = '/opt/app/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
