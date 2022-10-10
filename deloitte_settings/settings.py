import os
from decouple import config
from dj_database_url import parse

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DEBUG = config('DEBUG', default=False, cast=bool)

if ENVIRONMENT == 'development':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SECRET_KEY = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'
    ALLOWED_HOSTS = ['*']

else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ALLOWED_HOSTS = ['sistema-alunos.herokuapp.com']
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if ENVIRONMENT == 'development':

    INSTALLED_APPS = [
        # Django
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',

        # Django rest
        'rest_framework.authtoken',
        'rest_framework',

        # Imported Apps
        'storages',

        # Project Apps
        'apps.abstract',
        'apps.student',
        'apps.permissions',
        'apps.discipline',
        'apps.report_card',
    ]
else:
    INSTALLED_APPS = [
        # Django
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',

        # Django rest
        'rest_framework.authtoken',
        'rest_framework',

        # Imported Apps
        'storages',

        # Project Apps
        'apps.abstract',
        'apps.student',
        'apps.permissions',
        'apps.discipline',
        'apps.report_card',
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

ROOT_URLCONF = 'deloitte_settings.urls'

template = 'templates'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, template)],
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
WSGI_APPLICATION = 'deloitte_settings.wsgi.application'

if ENVIRONMENT == 'development':
    default_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    DATABASES = {'default': config('DATABASE_URL', default=default_url, cast=parse)}

else:
    DATABASES = {'default': config('CLEARDB_DATABASE_URL', cast=parse)}

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

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Statics Files Local Configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'static_in_env')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',

]

ASGI_APPLICATION = "deloitte_settings.asgi.application"

# LOGIN

LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/api/v1/docs/"
LOGIN_REDIRECT_URL = "/api/v1/docs/"
LOGOUT_URL = "/logout/"

# SITE ID
SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}
