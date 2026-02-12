#!/bin/bash
set -e

# Debug: log what's happening
echo "=== Starting deployment script ==="
echo "FLASK_APP=$FLASK_APP"

# Set Flask app for CLI commands
export FLASK_APP=wsgi:app

echo "Running flask db stamp..."
flask db stamp cc862af7b8f7 || echo "Stamp failed, continuing..."

echo "Running flask db upgrade..."
flask db upgrade || echo "Upgrade completed"

echo "Starting Gunicorn..."
exec gunicorn wsgi:app \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-2} \
    --timeout 120 \
    --log-file - \
    --access-logfile -

