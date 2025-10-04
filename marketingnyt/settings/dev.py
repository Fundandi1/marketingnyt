"""
Development settings for marketingnyt project.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = ["*"]

# Database - use SQLite for development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Disable cache in development
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Disable cache middleware in development
MIDDLEWARE = [m for m in MIDDLEWARE if "cache" not in m.lower()]

# Add django-extensions if available
try:
    import django_extensions
    INSTALLED_APPS += ["django_extensions"]
except ImportError:
    pass

# Development logging
LOGGING["root"]["level"] = "DEBUG"
LOGGING["loggers"]["django"]["level"] = "DEBUG"
