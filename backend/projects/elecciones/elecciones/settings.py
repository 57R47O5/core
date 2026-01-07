"""
Django settings for elecciones project.

Runtime-driven configuration.
This project does not define infrastructure.
"""

from pathlib import Path
import os
import sys
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv
# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------

# backend/projects/elecciones/elecciones/settings.py
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR.parents[1]  # .../backend
APPS_DIR = BACKEND_DIR / "apps"
ENV_PATH = BASE_DIR / ".env"

for p in (BACKEND_DIR, APPS_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    raise ImproperlyConfigured(f".env file not found at {ENV_PATH}")

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ImproperlyConfigured(f"Missing environment variable: {name}")
    return value


# -------------------------------------------------------------------
# Core settings
# -------------------------------------------------------------------

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env("DJANGO_DEBUG").lower() == "true"

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(",")


# -------------------------------------------------------------------
# Application definition
# -------------------------------------------------------------------

INSTALLED_APPS = [
    "corsheaders",
    "apps.base",
    "apps.auditoria",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "elecciones.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "elecciones.wsgi.application"


# -------------------------------------------------------------------
# Database (runtime-controlled)
# -------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}


# -------------------------------------------------------------------
# Authentication
# -------------------------------------------------------------------

AUTH_USER_MODEL = "base.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# -------------------------------------------------------------------
# Internationalization
# -------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# -------------------------------------------------------------------
# Static files
# -------------------------------------------------------------------

STATIC_URL = "static/"


# -------------------------------------------------------------------
# CORS / CSRF (runtime-controlled)
# -------------------------------------------------------------------

CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS").split(",")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS").split(",")
CORS_ALLOW_CREDENTIALS = True
