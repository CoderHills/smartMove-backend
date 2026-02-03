from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to values within the .ini file in use.
config = context.config

# interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import Base
# target_metadata = Base.metadata

# Import the Flask application and its database instance
import os, sys
from flask import current_app

sys.path.append(os.getcwd())
from app import create_app
from app.extensions import db

# ensure the Flask app is initialized
if current_app:
    target_app = current_app
else:
    target_app = create_app()

with target_app.app_context():
    target_metadata = db.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired a number of ways:
# In this case, we acquire the 'sqlalchemy.url' key using a
# combination of config.get_main_option (value set in the config file)
# and an environment variable (important for production deployment).
# this ensures that env.py works both when run directly by alembic,
# and when run from the Flask app (e.g. through Flask-Migrate).
def get_url():
    return target_app.config.get('SQLALCHEMY_DATABASE_URI')

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here send literal SQL
    statements to the producer.

    """
    url = get_url()
    context.configure(
        url=url,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario, we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()