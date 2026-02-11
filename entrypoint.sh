#!/bin/bash
set -e

echo "Running database migrations..."
flask db upgrade

echo "Migrations completed. Starting gunicorn..."
exec gunicorn wsgi:app --config gunicorn.conf.py

