#!/usr/bin/env python3
"""Run Alembic migrations programmatically using the Flask app's DB URL.

Usage:
  python scripts/run_migrations.py

On Railway you can run:
  railway run python scripts/run_migrations.py
"""
from app import create_app
from alembic.config import Config
from alembic import command


def run_migrations():
    app = create_app()
    with app.app_context():
        cfg = Config()
        # Use migrations directory in project root
        cfg.set_main_option("script_location", "migrations")
        # Ensure Alembic uses the same DB URL as Flask
        db_url = app.config.get("SQLALCHEMY_DATABASE_URI")
        if not db_url:
            raise RuntimeError("SQLALCHEMY_DATABASE_URI is not set in app config")
        cfg.set_main_option("sqlalchemy.url", db_url)

        print(f"Running migrations against: {db_url}")
        command.upgrade(cfg, "head")
        print("Migrations applied")


if __name__ == "__main__":
    run_migrations()
