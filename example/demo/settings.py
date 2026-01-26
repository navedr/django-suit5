"""
Django settings for demo project.
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the path so we can import django-suit5
sys.path.insert(0, os.path.dirname(BASE_DIR))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'demo-secret-key-not-for-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'suit5',  # Django Suit5 - must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'testapp',
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

ROOT_URLCONF = 'demo.urls'

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

WSGI_APPLICATION = 'demo.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Django Suit5 configuration
SUIT_CONFIG = {
    'ADMIN_NAME': 'Django Suit5 Demo',
    'HEADER_DATE_FORMAT': 'l, jS F Y',
    'HEADER_TIME_FORMAT': 'H:i',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
    'LIST_PER_PAGE': 20,
    'MENU_OPEN_FIRST_CHILD': True,
    'MENU': (
        'sites',
        {'app': 'auth', 'icon': 'bi bi-lock', 'models': ('user', 'group')},
        {'label': 'Test App', 'icon': 'bi bi-box', 'models': (
            {'model': 'testapp.category', 'icon': 'bi bi-folder'},
            {'model': 'testapp.product', 'icon': 'bi bi-bag'},
            {'model': 'testapp.order', 'icon': 'bi bi-cart'},
            {'model': 'testapp.customer', 'icon': 'bi bi-person'},
        )},
        {'label': 'Settings', 'icon': 'bi bi-gear', 'models': (
            {'model': 'testapp.sitesettings', 'icon': 'bi bi-sliders'},
        )},
    ),
}
