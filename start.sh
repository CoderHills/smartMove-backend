#!/bin/bash
set -e

echo "=== Starting deployment script ==="
echo "FLASK_APP=$FLASK_APP"

export FLASK_APP=wsgi:app

echo "Running flask db upgrade (creating tables)..."
flask db upgrade || echo "Upgrade completed"

echo "Starting Gunicorn..."
exec gunicorn wsgi:app \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-2} \
    --timeout 120 \
    --log-file - \
    --access-logfile -

