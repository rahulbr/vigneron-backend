# Replace the entire alembic/env.py with this clean version:
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Add your project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Import your models
from app.db.base import Base
from app.models.organization import Organization  # Import all your new models
from app.models.property import Property
from app.models.block import Block

# this is the Alembic Config object
config = context.config

# Set the database URL from environment
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:54322/postgres'))

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()