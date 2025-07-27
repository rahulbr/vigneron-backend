"""Add comprehensive agricultural data model

Revision ID: 8cc6a60563f6
Revises: 
Create Date: 2025-07-22 20:06:48.192290

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '8cc6a60563f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create ENUM types first
    op.execute("CREATE TYPE org_type_enum AS ENUM ('winery', 'vineyard', 'orchard', 'farm', 'coffee_estate', 'processing_facility')")
    op.execute("CREATE TYPE subscription_tier_enum AS ENUM ('free', 'basic', 'premium', 'enterprise')")
    op.execute("CREATE TYPE property_type_enum AS ENUM ('vineyard', 'orchard', 'ranch', 'farm', 'coffee_estate')")
    op.execute("CREATE TYPE crop_type_enum AS ENUM ('grape', 'apple', 'cherry', 'pear', 'coffee', 'avocado', 'citrus', 'stone_fruit', 'berry', 'nut', 'other')")
    
    # Create organizations table
    op.create_table('organizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('org_name', sa.String(length=100), nullable=False),
        sa.Column('org_type', postgresql.ENUM(name='org_type_enum'), nullable=False),
        sa.Column('agricultural_profile', sa.JSON(), nullable=True),
        sa.Column('ui_preferences', sa.JSON(), nullable=True),
        sa.Column('subscription_tier', postgresql.ENUM(name='subscription_tier_enum'), nullable=True),
        sa.Column('timezone', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('org_name')
    )
    
    # Add more tables here...

def downgrade():
    op.drop_table('organizations')
    op.execute("DROP TYPE IF EXISTS org_type_enum")
    op.execute("DROP TYPE IF EXISTS subscription_tier_enum")
    # Add more cleanup...