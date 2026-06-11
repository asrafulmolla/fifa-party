release: python manage.py migrate --noinput
web: gunicorn fifaparty.wsgi:application --bind 0.0.0.0:$PORT
