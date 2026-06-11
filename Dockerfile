FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Give permission to the user to write to /app (needed for HF Spaces)
RUN chown -R 1000:1000 /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY --chown=1000:1000 . .

# Hugging Face runs containers with user ID 1000
USER 1000

# Create staticfiles directory (if missing)
RUN mkdir -p /app/staticfiles

# Port 7860 is required by Hugging Face Spaces
EXPOSE 7860

# Run migrations, collect static files, and start the server
CMD python manage.py collectstatic --noinput && \
    python manage.py migrate --noinput && \
    gunicorn fifaparty.wsgi:application --bind 0.0.0.0:7860
