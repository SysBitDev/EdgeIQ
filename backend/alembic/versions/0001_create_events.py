"""create events table

Revision ID: 0001
Revises:
Create Date: 2025-09-19
"""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "events",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False, index=True),
        sa.Column("agent_id", sa.String(128), nullable=False, index=True),
        sa.Column("metric", sa.String(64), nullable=False, index=True),
        sa.Column("value", sa.Float, nullable=False),
        sa.Column("ts", sa.BigInteger, nullable=False, index=True),
    )


def downgrade() -> None:
    op.drop_table("events")
