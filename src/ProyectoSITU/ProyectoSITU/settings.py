"""
Django settings for ProyectoSITU project.
"""

from pathlib import Path
import os
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Logging setup
logger = logging.getLogger(__name__)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-af(gu6!2993md_qjot2c1pfwz=sb(q$-$xhnjhq^=_kkt@r@_7')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 'yes']

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

CSRF_TRUSTED_ORIGINS = [
    os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://boris-situ-hjdddag5hrffg8g5.centralus-01.azurewebsites.net'),
]

# =============================================================
# PERSISTENT DATA DIRECTORIES (Azure Compatible)
# Use /home/ as it's the only persistent directory in Azure App Service
# =============================================================
HOME_DIR = Path(os.environ.get('HOME', '/home/site/wwwroot'))
DATA_DIR = HOME_DIR / 'situ_data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_DIR = DATA_DIR / 'db'
DB_DIR.mkdir(parents=True, exist_ok=True)

MEDIA_DIR = DATA_DIR / 'media'
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

logger.info(f'Data directory: {DATA_DIR}')
logger.info(f'Database directory: {DB_DIR}')
logger.info(f'Media directory: {MEDIA_DIR}')

# =============================================================
# DATABASE CONFIGURATION
# SQLite stored in persistent /home/ directory
# =============================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(DB_DIR / 'db.sqlite3'),  # Convert Path to string for compatibility
    }
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800

# =============================================================
# STATIC FILES CONFIGURATION
# =============================================================
STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / 'staticfiles')
STATICFILES_DIRS = [str(BASE_DIR / 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =============================================================
# MEDIA FILES CONFIGURATION (User Uploads)
# =============================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = str(MEDIA_DIR)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appSITUweb',
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
    'appSITUweb.middleware.MediaFilesMiddleware',  # Serve media files from /home/
]

ROOT_URLCONF = 'ProyectoSITU.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR / 'templates')],
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

WSGI_APPLICATION = 'ProyectoSITU.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'