import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u2m$#v=rt4990)*3$cpdgd61cev-8sgpjo2ld&%$c(e$j&tx3*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['odonto.undb.edu.br']

INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'user',
    'box',
    'config', 
    'colorfield',
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

ROOT_URLCONF = 'core.urls'
AUTH_USER_MODEL = 'user.Usuario'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    
}

AUTH_PASSWORD_VALIDATORS = [
    #{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    #{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    #{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    #{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Fortaleza'
USE_I18N = True
USE_TZ = False
USE_L10N = True


STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


AUTHENTICATION_BACKENDS = (
    'gdbundbrm.api_rm.RmAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
 )

# Pacote gdbundbrm
RM_USER = ''
RM_PASS = ''
RM_API_PORT = ''
RM_BASE_URL = ''

LOGIN_REDIRECT_URL = 'base:index'
LOGOUT_REDIRECT_URL = 'base:login'
LOGIN_URL = 'base:login'
LOGIN_ERROR_URL = '/logout'

#send email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

NOTIFICAR = True
try:
    from .local_settings import *
except ImportError:
    pass
