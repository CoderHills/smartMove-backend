#!/bin/bash
set -e

# Set Flask app for CLI commands
export FLASK_APP=wsgi:app

# Try to stamp, if it fails (new DB), just continue
flask db stamp cc862af7b8f7 || true

# Always run migrations to create tables
flask db upgrade

# Start Gunicorn
exec gunicorn wsgi:app \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-2} \
    --timeout 120 \
    --log-file - \
    --access-logfile -

