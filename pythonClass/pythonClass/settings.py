"""
Django settings for pythonClass project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print "BASE_DIR=[", BASE_DIR

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'or2x0&7-fwu-o@82i0q+5qzauq%a*il^*9@&ibzx6degf#fxem'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
###    'django.contrib.admin',
###    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
###    'django.contrib.auth.middleware.AuthenticationMiddleware',
###    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
###    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'pythonClass.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
###                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pythonClass.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'visitors',
#        'HOST': 'www.parkwhileaway.com',                                                 
        'HOST': 'dev.svcvllc.com',
        #'HOST': 'SNCSMENG03',                                                 
        'PORT': '3306',
        'USER': 'python',
        'PASSWORD': 'ucscext'    

#                    }
    }
}
'''
#############################MongoDB settings
import mongoengine
DATABASES = {
    'default': {
        'ENGINE' : 'django_mongodb_engine',
        'NAME': 'visitors',
    }
}
#DBName = "visitors"
#MONGO_DATABASE_NAME = 'visitors'

#from mongoengine import connect, register_connection
#connect('visitors')
#register_connection('default', MONGO_DATABASE_NAME)
###################################################################

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT= os.path.join(BASE_DIR, 'webapp/static')
print 'STATIC_ROOT=[', STATIC_ROOT

STATICFILES_DIRS = (
    #os.path.join(STATIC_ROOT, 'static'),
    #'C:/github/trunk/pyMySQL/myapp/static',
    #'/var/www/pyMySQL/myapp/static',
    #'/home/ec2-user/downloads/pyMySQL/myapp/static',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ("js", os.path.join(STATIC_ROOT,'js')),
    ("css", os.path.join(STATIC_ROOT,'css')),
    ("images", os.path.join(STATIC_ROOT,'images')),
)