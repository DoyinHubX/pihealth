"""
Django settings for o10_book_crudauth project.

Generated by 'django-admin startproject' using Django 4.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Import dj-database-url at the beginning of the file.
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

SECRET_KEY = "django-insecure-s*hg*lxwx#udzcp%trlvg7q%$ehr%a=mggx)+lb91=39=rj@o_"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'books',
    'heartrisk',
    'widget_tweaks',
    'crispy_forms',
    'crispy_bootstrap4',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

from django.contrib.messages import constants as messages
# Configure message tags for Bootstrap compatibility
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',  # Optional: Use 'secondary' for debug messages
    messages.INFO: 'info',        # Default blue info messages
    messages.SUCCESS: 'success',  # Green for success
    messages.WARNING: 'warning',  # Yellow for warnings
    messages.ERROR: 'danger',     # Red for errors
}

ROOT_URLCONF = "o10_book_crudauth.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "o10_book_crudauth.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


# Replace the SQLite DATABASES configuration with PostgreSQL:
DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators


postgres://ngvmhgra:3dP2vWmYpZcA2-kf3iEOqu6UAhu7ij29@kandula.db.elephantsql.com/ngvmhgra

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

#STATIC_URL = "static/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# This setting informs Django of the URI path from which your static files will be served to users
# Here, they well be accessible at your-domain.onrender.com/static/... or yourcustomdomain.com/static/...
STATIC_URL = '/static/'

# The location to collect static files (e.g., on production)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# This production code might break development mode, so we check whether we're in DEBUG mode
if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


AUTH_USER_MODEL = 'books.CustomUser'

# Redirect to home page after login
LOGIN_REDIRECT_URL = '/heartrisk/predict/'
LOGIN_URL = '/login/'  # Custom login URL

CRISPY_TEMPLATE_PACK = 'bootstrap4'  # Options: bootstrap, bootstrap3, bootstrap4, tailwind, etc.

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
