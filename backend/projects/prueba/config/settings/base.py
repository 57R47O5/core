"""
Django settings for prueba project.

Runtime-driven configuration.
Apps are managed by ORCO.
"""

from pathlib import Path
import os
import sys
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[3]

BACKEND_DIR = Path(
    os.environ.get("BACKEND_DIR", BASE_DIR)
).resolve()

APPS_DIR = BACKEND_DIR / "apps"

for p in (BACKEND_DIR, APPS_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

ENV_PATH = BASE_DIR / "prueba" / ".env"

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

from .orc_apps import ORC_APPS

DJANGO_BASE_APPS = [
    "corsheaders",
    "rest_framework",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = DJANGO_BASE_APPS + ORC_APPS

# -------------------------------------------------------------------
# Middleware
# -------------------------------------------------------------------

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "auth.middleware.token.AuthTokenMiddleware",    
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "prueba.urls"

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

WSGI_APPLICATION = "projects.prueba.prueba.wsgi.application"

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
