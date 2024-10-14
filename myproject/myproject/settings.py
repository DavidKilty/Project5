import environ
from pathlib import Path
import os
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))  

STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY')


SECRET_KEY = 'django-insecure-6kl*+q-t(&75*l6mcrn4o@$!8sm(nw%h805dy2*@bk0u_31=l*'

DEBUG = True

ALLOWED_HOSTS = ['8000-davidkilty-project5-of8fv53e6w4.ws.codeinstitute-ide.net',
                  'nightspot.herokuapp.com', 
                  'nightspot.onrender.com' ,
                  
]

CSRF_TRUSTED_ORIGINS = [
    'https://8000-davidkilty-project5-of8fv53e6w4.ws.codeinstitute-ide.net'
]



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'payments',
    'django.contrib.sitemaps',
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

ROOT_URLCONF = 'myproject.myproject.urls'

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

WSGI_APPLICATION = 'myproject.myproject.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
USE_TZ = True

BASE_DIR = Path(__file__).resolve().parent.parent

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  

STATICFILES_DIRS = [
    BASE_DIR.parent / 'payments' / 'static',
]


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STRIPE_WEBHOOK_SECRET = 'whsec_6a835389f61eb2a820c0d6ccecef8bd9ab7c3b35df4aa4dadc443c80cea3e416' 

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = 'ticket_list'  

LOGOUT_REDIRECT_URL = 'login'  

import django_heroku
django_heroku.settings(locals())


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'nightspotoperations@gmail.com'
EMAIL_HOST_PASSWORD = 'npuaptrrfhwhaptu'  
DEFAULT_FROM_EMAIL = 'nightspotoperations@gmail.com'
BREVO_API_KEY = env('BREVO_API_KEY')

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}
