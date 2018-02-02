"""
Django settings for Photash project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$mc!7too13@9(t+%ka@%$+afm3*zx$@8544ltd76x*%_ezx9sz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Django uygulamaları
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Kendi uygulamalarım
    'home',
    'user',
    'contest',
    'photo',
    'reportedPhotos',
    #3. parti uygulamalar
    'star_ratings',
    'crispy_forms',
    'captcha',
    'rest_framework',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Photash.login_logout_middleware.LoginRequiredMiddleware'
]

ROOT_URLCONF = 'Photash.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Photash.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'tr'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
'''STATIC_ROOT = os.path.join(BASE_DIR, 'static')'''
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


MEDIA_ROOT = (BASE_DIR)
MEDIA_URL = '/media/'

'''DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'''
#Artık bunu kullanmıyorum. ResizedImage upload esnasında orijinali almıyor, boyutunu küçültüp alıyor.

STAR_RATINGS_RERATE = False
STAR_RATINGS_RANGE = 10

CRISPY_TEMPLATE_PACK = 'bootstrap3'

RECAPTCHA_PUBLIC_KEY  = '6LcPxzwUAAAAAP1Oz-VlEtxrBaUAo8J9NsVmyHFZ'
RECAPTCHA_PRIVATE_KEY = '6LcPxzwUAAAAANQU8KLT5z4xfoR5kzrTAXSf85pY'

# şirket maili aldıktan sonra değiştirilecek, şimdilik kendi mailimi yazdım.
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'yourmail@gmail.com' # yourmail
EMAIL_HOST_PASSWORD = 'yourpassword' # yourpassword
EMAIL_PORT = 587

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 3
}

#Logged in userların redirect edileceği sayfa urli
LOGIN_REDIRECT_URL = '/user/profile'

LOGIN_URL = '/user/login/'

#Logged in user'ların erişemeyeceği urller. Yani sadece misafirlerin erişebileceği urller.
LOGIN_EXEMPT_URLS= (
    r'^user/logout/$',
    r'^user/register/$'
)

#Hem logged in userların hem logged out userların ulaşabileceği urller
COMMON_URLS = (
    r'^$',
    r'^contest/(?P<slug>[\w-]+)/photos/$',  #Contest photopool
    r'^contest/index/$',            #Contest index
    r'^contest/(?P<slug>[\w-]+)/$', #Contest detail
    r'^photo/(?P<id>\d+)/$', #Photo detail
    r'^ratings/(?P<content_type_id>\d+)/(?P<object_id>\d+)/', #Ratings
    r'^media/(?P<path>.*)$',
    r'^static/(?P<path>.*)$',
)