#!/bin/bash
set -e

echo "=== Starting deployment script ==="
export FLASK_APP=wsgi:app

# Create tables directly using SQLAlchemy (more reliable than migrations)
echo "Creating database tables..."
python scripts/create_tables.py

echo "Starting Gunicorn..."
exec gunicorn wsgi:app \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-2} \
    --timeout 120 \
    --log-file - \
    --access-logfile -

