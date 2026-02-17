"""create transactions table

Revision ID: 3b62eb4523e1
Revises: 
Create Date: 2026-02-17 15:57:38.140880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b62eb4523e1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Text, nullable=False),
        sa.Column("amount", sa.Integer, nullable=False),
        sa.Column("type", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("NOW()"), nullable=False)
    )


def downgrade() -> None:
    op.drop_table("transactions")
