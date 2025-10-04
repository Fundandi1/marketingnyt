"""
Local development settings with PostgreSQL.
"""

from .dev import *

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'marketingnyt_local',
        'USER': os.getenv('DB_USER', os.getenv('USER')),  # Use your macOS username
        'PASSWORD': os.getenv('DB_PASSWORD', ''),  # No password for local development
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Add visual indicator (only in interactive mode)
import sys
if sys.stdout.isatty():
    print(f"🐘 Using PostgreSQL database: {DATABASES['default']['NAME']}")
    print(f"🐘 Database user: {DATABASES['default']['USER']}")

# Disable debug logging for management commands
import logging
if 'manage.py' in sys.argv and any(cmd in sys.argv for cmd in ['dumpdata', 'loaddata']):
    logging.disable(logging.DEBUG)
