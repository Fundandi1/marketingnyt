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

print(f"🐘 Using PostgreSQL database: {DATABASES['default']['NAME']}")
print(f"🐘 Database user: {DATABASES['default']['USER']}")
