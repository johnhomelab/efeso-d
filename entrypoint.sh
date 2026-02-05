#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for Postgres
echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Execute the passed command (e.g., gunicorn)
exec "$@"
