"""
Django settings for fifaparty project — FIFA Watch Party Finder Bangladesh.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fifa-party-bd-2026-key-change-in-production')

# On Vercel, disable DEBUG and use secure settings
IS_VERCEL = os.environ.get('VERCEL', False)
DEBUG = not IS_VERCEL and os.environ.get('DEBUG', 'True') == 'True'

_extra_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')
ALLOWED_HOSTS = list(filter(None, [
    'localhost',
    '127.0.0.1',
    '.vercel.app',
    '.onrender.com',
    '.pythonanywhere.com',
    'mdasrafulmolla.pythonanywhere.com',
    _extra_host,
]))

CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://*.onrender.com',
    'https://*.pythonanywhere.com',
    'https://mdasrafulmolla.pythonanywhere.com',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'core',
    'venues',
    'matches',
    'accounts',
    'notifications',
    'predictions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fifaparty.urls'

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
                'notifications.context_processors.notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'fifaparty.wsgi.application'

# On Vercel the filesystem is read-only; use /tmp for SQLite
_DB_PATH = Path('/tmp') / 'db.sqlite3' if os.environ.get('VERCEL') else BASE_DIR / 'db.sqlite3'

DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{_DB_PATH}',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# If using PostgreSQL (Neon), enforce SSL
if DATABASES['default'].get('ENGINE') == 'django.db.backends.postgresql':
    DATABASES['default'].setdefault('OPTIONS', {})
    DATABASES['default']['OPTIONS']['sslmode'] = 'require'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'  # Bangladesh Standard Time
USE_I18N = True
USE_TZ = True

# Static & Media
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# On Vercel the project root is read-only; write collected files to /tmp
STATIC_ROOT = Path('/tmp/staticfiles') if IS_VERCEL else BASE_DIR / 'staticfiles'
# Use CompressedStaticFilesStorage on Vercel (no manifest needed — avoids crash
# when staticfiles/ hasn't been collected). Use CompressedManifest locally.
if IS_VERCEL:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# External APIs
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', 'YOUR_GOOGLE_MAPS_API_KEY')
FOOTBALL_DATA_API_KEY = os.environ.get('FOOTBALL_DATA_API_KEY', 'YOUR_FOOTBALL_DATA_API_KEY')
