import os
from pathlib import Path
import json
import environ

# Optional AWS Secrets Manager support
try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
except Exception:
    boto3 = None
    BotoCoreError = Exception
    ClientError = Exception

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY', default='django-secret-key-for-dev')
DEBUG = env('DEBUG', default=True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
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

ROOT_URLCONF = 'prod_django_project_aws.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'prod_django_project_aws.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME', default='ecommerce'),
        'USER': env('DATABASE_USER', default='ecommerce_user'),
        'PASSWORD': env('DATABASE_PASSWORD', default='ecommerce_pass'),
        'HOST': env('DATABASE_HOST', default='db'),
        'PORT': env('DATABASE_PORT', default='5432'),
    }
}

# Development fallback to SQLite when DATABASE_NAME is not configured or
# the PostgreSQL connection is unavailable.
if env.bool('USE_SQLITE', default=False):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Load secrets from AWS Secrets Manager when enabled. Secrets should be stored
# as a JSON object, for example:
# {"SECRET_KEY": "...", "DATABASE_NAME": "...", "DATABASE_USER": "...", "DATABASE_PASSWORD": "...", "DATABASE_HOST": "...", "DATABASE_PORT": "..."}
def _load_aws_secret(secret_id: str):
    if not boto3 or not secret_id:
        return {}
    try:
        client = boto3.client('secretsmanager')
        resp = client.get_secret_value(SecretId=secret_id)
        secret_string = resp.get('SecretString')
        if secret_string:
            return json.loads(secret_string)
    except (BotoCoreError, ClientError):
        pass
    return {}

if env.bool('USE_AWS_SECRETS', default=False):
    secret_id = env('AWS_SECRET_ID', default=None)
    aws_secret = _load_aws_secret(secret_id)
    if aws_secret:
        # Override Django settings with values from the secret when present
        SECRET_KEY = aws_secret.get('SECRET_KEY', SECRET_KEY)
        # Database overrides
        db_name = aws_secret.get('DATABASE_NAME')
        if db_name:
            DATABASES['default'].update({
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': aws_secret.get('DATABASE_NAME', DATABASES['default'].get('NAME')),
                'USER': aws_secret.get('DATABASE_USER', DATABASES['default'].get('USER')),
                'PASSWORD': aws_secret.get('DATABASE_PASSWORD', DATABASES['default'].get('PASSWORD')),
                'HOST': aws_secret.get('DATABASE_HOST', DATABASES['default'].get('HOST')),
                'PORT': aws_secret.get('DATABASE_PORT', DATABASES['default'].get('PORT')),
            })

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
