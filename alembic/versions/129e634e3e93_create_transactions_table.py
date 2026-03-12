"""create transactions table

Revision ID: 129e634e3e93
Revises: 3b62eb4523e1
Create Date: 2026-03-12 13:57:52.281333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '129e634e3e93'
down_revision: Union[str, None] = '3b62eb4523e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
