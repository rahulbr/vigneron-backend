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
from app.models.organization import Organization
from app.models.property import Property
from app.models.block import Block
from app.models.row import Row
from app.models.individual_vine import IndividualVine
from app.models.user import User
from app.models.activity import Activity
from app.models.crop_specific_data import CropSpecificData
from app.models.spray_product import SprayProduct
from app.models.financial_transaction import FinancialTransaction

# this is the Alembic Config object
config = context.config

# Set the database URL from environment
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL', 'postgresql://postgres:@localhost:5432/vigneron_backend'))

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
        compare_type=True,
        compare_server_default=True,
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
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()