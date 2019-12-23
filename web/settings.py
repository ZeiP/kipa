# encoding: utf-8
import os

hakemisto = os.path.normpath(os.path.dirname(__file__))
tarkistus = os.getcwd()

DEBUG = False
RECORDING=False
if not hakemisto == tarkistus :
        #Viittaisi siihen etta kyseessa on apachen alta toimiva, joten pakotetaan debugit pois
        DEBUG=False

ADMINS = (
     #('frans korhonen', 'frans.korhonen@gmail.com'),
)

MANAGERS = ADMINS

'''
DATABASE_ENGINE = 'django.db.backends.sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = hakemisto + '/tupa.db'     # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(hakemisto, 'tupa.db'),
    }
}


# Cache
TAUSTALASKENTA = False # Tulokset lasketaan taustalla (Vaatii toimiakseen tomivan cachekokoonpanon)
CACHE_TULOKSET = False # Etsitaanko tuloksia cachesta
CACHE_TULOKSET_TIME = 1800 # Tuloscachen voimassaoloaika viimeisesta nayttokerrasta. [s]
#CACHE_BACKEND = 'locmem:///' # Cache system for developement
#CACHE_BACKEND = 'locmem:///' # Cache system for developement
CACHE_BACKEND = 'db://tupa_tulos_cache'
if not CACHE_TULOKSET : 
        CACHE_BACKEND = 'dummy:///' # No cache in use
        TAUSTALASENTA = False

# Local time zone for this installation. 
TIME_ZONE = 'Europe/Helsinki'

# Language code for this installation. 
LANGUAGE_CODE = 'en-US'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False
'''
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = hakemisto + "/media/"

STATIC_DOC_ROOT = hakemisto + "/media/"

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''
'''
FILE_UPLOAD_HANDLERS= ("django.core.files.uploadhandler.MemoryFileUploadHandler",
 "django.core.files.uploadhandler.TemporaryFileUploadHandler",)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'shbtq($_^om(xep=5f97k2+ntb3!cqn+)%8r#s6udzqnhj$5p6'

'''
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)
'''
'''
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
'''
ROOT_URLCONF = 'urls'

'''
TEMPLATE_DIRS = (
    hakemisto + '/templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
'''

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'tupa',
    'user_management',
    'django.contrib.admin',
    #'django.contrib.formtools',
    'django.template',
    #'django.contrib.databrowse'
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [hakemisto + '/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LOGIN_URL = ('/kipa/')
LOGIN_REDIRECT_URL = ('/kipa/')

TEST_RUNNER = ('tupa.tests.run_one_fixture')


STATIC_URL = '/kipamedia/'
STATIC_ROOT = os.path.join(hakemisto, "media")
'''
STATICFILES_DIRS = [
    os.path.join(hakemisto, "media"),
]
'''
#ALLOWED_HOSTS = ['127.0.0.1'] # Määritä tähän kaikki palvelimesi IP-osoitteet pilkulla erotettuna
ALLOWED_HOSTS = ['*'] # Salli kaikki yhteydet

WSGI_APPLICATION = 'wsgi.application'

DATA_UPLOAD_MAX_NUMBER_FIELDS = None # maaritaVartiot floodaa GET/POST:in

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
# Ottamalla käyttöön salasanan laatusäännöt, järjestelmä pakottaa käyttäjät käyttämään turvallisempia salasanoja
'''
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
'''
#HTTPS is not availible on devserver
#HTTPS would need sertificates to the web server program
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True
#SECURE_SSL_REDIRECT = True
