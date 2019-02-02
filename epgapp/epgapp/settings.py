import os
import posixpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_NAME = 'epgapp'
APP_DIR  = os.path.join(BASE_DIR, APP_NAME)
WSGI_APPLICATION = APP_NAME + '.wsgi.application'
LOGIN_REDIRECT_URL = 'home-link'
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a40eb3b4-fde5-4d71-8e91-26184e320329'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['epgapp.kodibg.org','localhost']

# Application definition
INSTALLED_APPS = [
    APP_NAME,
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = APP_NAME + '.urls'

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



# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))

LOGGING = {
 'version': 1,
 'disable_existing_loggers': False,
 'formatters': {
   'verbose': {
     'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
   },
   'simple': {
     'format': '%(levelname)s %(message)s'
   }
 },
 'handlers': {
   'console': {
     'level': 'DEBUG',
     'class': 'logging.StreamHandler',
     'formatter': 'verbose'
   },
   'file': {
     'level': 'DEBUG',
     'class': 'logging.FileHandler',
     'formatter': 'verbose',
     'filename': 'epgapp/logs/debug.txt',
   },
 },
 'loggers': {
   APP_NAME: {
     'handlers': ['file'],
     'level': 'DEBUG'
   },
   'django': {
     'handlers': ['file'],
     'level': 'ERROR',
     'propagate': True,
   },
   'django.db.backends': {
     'handlers': ['file'],
     'level': 'ERROR',
     'propagate': False,
   },
 },
}
