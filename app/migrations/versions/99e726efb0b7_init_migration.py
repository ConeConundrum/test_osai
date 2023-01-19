"""init migration

Revision ID: 99e726efb0b7
Revises:
Create Date: 2023-01-18 20:23:04.333861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99e726efb0b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'url',
        sa.Column('id', sa.BIGINT, nullable=False, primary_key=True),
        sa.Column('original_url', sa.String(length=2083), unique=True, nullable=False),
        sa.Column('short_url', sa.String(length=255), unique=True, nullable=False),
        sa.Column('key', sa.String(length=36), unique=True, nullable=False)
    )
    op.create_index('key_index', table_name='url', columns=['key'], unique=True)


def downgrade():
    op.drop_index('key_index', table_name='url')
    op.drop_table('url')
