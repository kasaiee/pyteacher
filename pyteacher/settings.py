"""
Django settings for pyteacher project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from zeep import Client

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*#0o07nr!p3h&@e5@tr%f5683#(nh)#6(hi%v5bjuw9#cr8qx4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'materialize',
    'crispy_forms',
    'crispy_forms_materialize',
    'rest_framework',
    'rest_framework.authtoken',
    'ckeditor',
    'ckeditor_uploader',
    'social_django',
    'sorl.thumbnail',
    'genericadmin',
    'django_social_share',

    'app_base',
    'app_accounts',
    'app_chat',
    'app_api',
    'app_social',
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

ROOT_URLCONF = 'pyteacher.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'pyteacher.context_processors.get_settings_value'
            ],
        },
    },
]

WSGI_APPLICATION = 'pyteacher.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

if DEBUG:
    # local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mydb',
            'USER': 'myuser',
            'PASSWORD': 'mypass',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
else:
    # deploy
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'pyteacher_db',
            'USER': 'pyteacher_db_user',
            'PASSWORD': '1',
            'HOST': 'localhost',
            'PORT': '',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR + '/static/'

MEDIA_ROOT = BASE_DIR + '/media/'

MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',  # for Google authentication
    'social_core.backends.github.GithubOAuth2',  # for Github authentication
    'social_core.backends.facebook.FacebookOAuth2',  # for Facebook authentication
 
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'app-base:home'
LOGIN_REDIRECT_URL = 'app-base:home'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '234046930740-vdrt3jj2jejki24l9t7b5amgvki1emk0.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '3SR37MU-lI5nXsg-J-lueKrJ'

SOCIAL_AUTH_GITHUB_KEY = '82c076af3f9d853e7492'
SOCIAL_AUTH_GITHUB_SECRET = '61a7b68db93d90c198e2eac912ecfb28554876ad'

CKEDITOR_UPLOAD_PATH = 'ck/uoloads/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

ALLOWED_SOCIAL_OBJECTS = ('Course', 'CourseSession', 'CourseSessionExercise', 'Comment')

DEFAULT_USER_AVATAR = STATIC_URL + 'img/default-user.jpg'

MERCHANT = os.environ['zarincode']
CLIENT = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
