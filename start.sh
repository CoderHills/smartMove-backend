#!/bin/bash
set -e

# Set Flask app for CLI commands
export FLASK_APP=wsgi:app

# Stamp database to current revision to skip old broken migrations
flask db stamp cc862af7b8f7

# Run any pending migrations
flask db upgrade

# Start Gunicorn with config file
# PORT is provided by Render/Heroku, fallback to 8000 for local
exec gunicorn wsgi:app \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-2} \
    --timeout 120 \
    --log-file - \
    --access-logfile -

