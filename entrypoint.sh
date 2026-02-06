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

# Prevent runserver
if echo "$@" | grep -q "runserver"; then
    echo "Error: 'runserver' is disabled. Use 'gunicorn' or another production server."
    exit 1
fi

# Execute the passed command (e.g., gunicorn)
exec "$@"
