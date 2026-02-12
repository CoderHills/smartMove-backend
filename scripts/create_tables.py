#!/usr/bin/env python3
"""Create all database tables directly using SQLAlchemy."""
import sys
sys.path.insert(0, '/app')

from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    print("Creating all database tables...")
    db.create_all()
    print("Tables created successfully!")
    
    # List all tables
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")

