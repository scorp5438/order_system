import os
from logging.config import dictConfig
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ для подписи cookies и других целей безопасности.
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-ky-$7g9_$ylp4pd194)6to@b-$*!n^ct9qfl$_k&wf@2+jy(xf'
)

# Режим отладки. Включает подробные ошибки и отключает кэширование.
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',

    'orders.apps.OrdersConfig',
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

ROOT_URLCONF = 'order_system.urls'

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

WSGI_APPLICATION = 'order_system.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_NAME_DB', 'test_order_db'),
        'USER': os.getenv('POSTGRES_USER_NAME', 'test_order_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'test_password'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', 5001)
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.'
                'password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
                'password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
                'password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
                'password_validation.'
                'NumericPasswordValidator',
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

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.'
                                'pagination.'
                                'PageNumberPagination',
    'PAGE_SIZE': 10,
}

logs_dir = os.path.join(BASE_DIR, 'logs')
os.makedirs(logs_dir, exist_ok=True)

logging_config = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': os.getenv('LOG_LEVEL_STREAM', 'DEBUG'),
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': os.getenv('LOG_LEVEL_FILE', 'INFO'),
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(BASE_DIR, 'logs', 'order_app.log'),
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 5,
            'encoding': 'utf8'
        },
    },
    'loggers': {
        'console_logger': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'file_logger': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

dictConfig(logging_config)
# URL для подключения к брокеру сообщений Celery (Redis).
CELERY_BROKER_URL = f'redis://{os.getenv("REDIS_HOST", "localhost")}:6379/0'
CELERY_RESULT_BACKEND = f'redis://{os.getenv(
    "REDIS_HOST",
    "localhost"
)}:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# Бэкенд для отправки электронной почты через SMTP.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'order_system@mail.ru'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = 'order_system@mail.ru'
