import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'u2m$#v=rt4990)*3$cpdgd61cev-8sgpjo2ld&%$c(e$j&tx3*'
#DEBUG = True
#ALLOWED_HOSTS = ['*']

DATABASES = {
    'default_local': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'pyodonto',
        'USER': 'rm',
        'PASSWORD': 'rm',
        'HOST': '10.235.30.17',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}

# Pacote gdbundbrm
RM_USER = ''
RM_PASS = ''
RM_API_PORT = '8051'
RM_BASE_URL = 'http://portal.undb.edu.br'

LOGIN_REDIRECT_URL = 'base:index'
LOGOUT_REDIRECT_URL = 'base:login'
LOGIN_URL = 'base:login'
LOGIN_ERROR_URL = '/logout'

#send email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = 'SUBJECT'
EMAIL_HOST_USER = ''
DEFAULT_FROM_EMAIL = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True

NOTIFICAR = True

try:
    from .local_settings import *
except ImportError:
    pass
