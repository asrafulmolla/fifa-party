"""
Vercel serverless entry point for the FIFA Party Django app.
Handles path setup, migrations, and DB seeding on cold start.
"""
import sys
import os

# Ensure the project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fifaparty.settings')

import django
django.setup()

# On Vercel, /tmp/db.sqlite3 is fresh on every cold start — migrate + seed
from django.core.management import call_command
from django.db import connection

try:
    # Check if tables exist by querying the matches table
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM matches_match")
except Exception:
    # Tables don't exist — run migrations and seed
    try:
        call_command('migrate', '--run-syncdb', verbosity=0)
        call_command('seed_matches', verbosity=0)
    except Exception as e:
        # Log but don't crash — app can still serve static pages
        print(f"[vercel] startup error: {e}")

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
