#!/bin/bash
set -e

export FLASK_APP=wsgi:app
export DATABASE_URL

# Stamp database to current revision to skip old migrations
flask db stamp cc862af7b8f7

# Run any pending migrations
flask db upgrade

# Start Gunicorn
exec gunicorn wsgi:app \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-2} \
    --timeout 120 \
    --log-file - \
    --access-logfile -

