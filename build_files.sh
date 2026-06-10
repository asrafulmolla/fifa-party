#!/bin/bash
# Build script for Vercel — runs collectstatic so WhiteNoise can serve files
python manage.py collectstatic --noinput
