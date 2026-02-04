FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required by some Python packages (e.g. psycopg2)
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	   build-essential \
	   gcc \
	   libpq-dev \
	&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application source
COPY . /app

# Create a non-root user and adjust ownership
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Use $PORT if provided by the environment (Railway), fallback to 8000
CMD ["sh", "-c", "flask db upgrade && gunicorn run:app --bind 0.0.0.0:${PORT:-8000} --workers 3 --log-file -"]