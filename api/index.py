"""
Vercel serverless entry point for the FIFA Party Django app.
"""
import sys
import os

# Ensure the project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fifaparty.settings')
os.environ.setdefault('VERCEL', '1')

import django
django.setup()

# On Vercel, run migrations + seed on cold start only when using SQLite (/tmp)
# When DATABASE_URL is set (PostgreSQL), migrations are handled separately.
from django.conf import settings

_using_sqlite = 'sqlite' in settings.DATABASES['default'].get('ENGINE', '')

if _using_sqlite:
    from django.core.management import call_command
    from django.db import connection

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM matches_match")
    except Exception:
        try:
            call_command('migrate', '--run-syncdb', verbosity=0)
            call_command('seed_matches', verbosity=0)
        except Exception as e:
            print(f"[vercel] startup error: {e}")

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
