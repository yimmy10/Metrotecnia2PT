"""
Django settings for Metrotecnia project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=ho5^cnyt3sc0u^!kbj-ky%519w(pw6xc11%q1v&^fb*z@gx3*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'django.contrib.staticfiles',
    'channels',
    'channels_redis',
    'rest_framework',
    'django_select2',
    'widget_tweaks',
    'web',
    'Metrotecnia',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django_plotly_dash.middleware.BaseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CHANNEL_LAYERS = {
   'default': { 'BACKEND': 'channels_redis.core.RedisChannelLayer',
                'CONFIG': {
                           'hosts': [('127.0.0.1', 6379),],
                          }
              }
}

#STATICFILES_FINDERS = [
    
 #   'django_plotly_dash.finders.DashAssetFinder',
  #  'django_plotly_dash.finders.DashComponentFinder'
#]
# Add PLOTLY_COMPONENTS
PLOTLY_COMPONENTS = [
    'dash_core_components',
    'dash_html_components',
    'dash_renderer',
    'dpd_components']

X_FRAME_OPTIONS = 'SAMEORIGIN'


ROOT_URLCONF = 'Metrotecnia.urls'

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

WSGI_APPLICATION = 'Metrotecnia.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# if DEBUG:
#     DATABASES = {
#         # 'default': {
#         #     'ENGINE': 'django.db.backends.sqlite3',
#         #     'NAME': BASE_DIR / 'db.sqlite3',
#         # }

#         'default': {
#              'ENGINE': 'django.db.backends.mysql',
#              'NAME': 'ysgerman$metrotecnia',
#              'USER': 'root',
#              'PASSWORD': 'root',
#              'HOST': 'localhost',
#              'PORT': '3307',
#         }
#     }
# else:
#     DATABASES = {
#         # 'default': {
#         #     'ENGINE': 'django.db.backends.mysql',
#         #     'NAME': 'ysgerman$metrotecnia',
#         #     'USER': 'root',
#         #     'PASSWORD': 'root',
#         #     'HOST': 'localhost',
#         #     'PORT': '3307',
#         #}

#           'default': {
#              'ENGINE': 'django.db.backends.sqlite3',
#              'NAME': BASE_DIR / 'db.sqlite3',
#          }
#     }
if DEBUG:
    DATABASES = {
        'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'ysgerman$metrotecnia',
             'USER': 'root',
             'PASSWORD': 'root',
             'HOST': 'localhost',
             'PORT': '3307',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_datatables.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    'PAGE_SIZE': 50,
    'DATETIME_FORMAT': "%d/%m/%Y %I:%M:%S %p",
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL='/'
LOGIN_URL='/login'
LOGOUT_REDIRECT_URL='/login'

SESSION_EXPIRE_SECONDS = 3600  # 1 hora