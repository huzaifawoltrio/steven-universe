"""add_electronegativity_column

Revision ID: 4604563dca89
Revises: 125c11d680fa
Create Date: 2025-10-22 17:51:33.450886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4604563dca89'
down_revision: Union[str, Sequence[str], None] = '125c11d680fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('atoms', sa.Column('electronegativity', sa.Float(), nullable=True, comment='Pauling electronegativity value.'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('atoms', 'electronegativity')
