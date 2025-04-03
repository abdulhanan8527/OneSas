"""
Django settings for OneSas project.
Production-ready configuration for Railway.app.
"""

import os
from pathlib import Path
import dj_database_url  # For PostgreSQL

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# ===== Security =====
SECRET_KEY = os.environ.get('SECRET_KEY', 'yx6-0in=myys^n9q^$$2ywied=mkn+&!o%u^r^!a_btd@awk4i')  # Set in Railway Variables
DEBUG = os.environ.get('DEBUG', 'False') == 'True'  # False in production
ALLOWED_HOSTS = ['1sas.co', 'www.1sas.co', '*.railway.app']  # Replace with your domain
CSRF_TRUSTED_ORIGINS = ['https://1sas.co', 'https://www.1sas.co', 'https://*.railway.app']

# HTTPS Settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ===== Application Definition =====
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'OneSas_app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'OneSas.urls'
WSGI_APPLICATION = 'OneSas.wsgi.application'

# ===== Database =====
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('postgresql://postgres:QkwUVspBmOAUtVyBTANJssiRmpykXAVC@postgres.railway.internal:5432/railway'),
        conn_max_age=600
    )
}

# ===== Static & Media Files =====
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ===== Templates =====
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

# ===== Password Validation =====
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===== Internationalization =====
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ===== Default Auto Field =====
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'