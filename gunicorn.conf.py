import os

# Bind to PORT from environment (Render/Heroku), fallback to 8000
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

# Workers: Use env var or default to 2 (safe for Render free tier)
# Avoid CPU-based calculation as it can spawn too many workers on shared hosts
workers = int(os.environ.get('GUNICORN_WORKERS', '2'))

# Access and Error logs
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get('LOG_LEVEL', 'info')

# Timeout for long calculations (like distance matrices)
timeout = 120

# Graceful timeout for worker restart
graceful_timeout = 30

# Preload app for faster worker startup and memory sharing
preload_app = True
