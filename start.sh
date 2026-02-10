#!/bin/bash
set -e

# Set Flask app for CLI commands
export FLASK_APP=wsgi:app

# Run Flask database migrations
flask db upgrade

# Start Gunicorn with config file
# PORT is provided by Render/Heroku, fallback to 8000 for local
exec gunicorn wsgi:app \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-2} \
    --timeout 120 \
    --log-file - \
    --access-logfile -
