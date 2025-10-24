"""add_ionization_energy_column

Revision ID: 125c11d680fa
Revises: 687159da0351
Create Date: 2025-10-22 17:17:55.184887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '125c11d680fa'
down_revision: Union[str, Sequence[str], None] = '687159da0351'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('atoms', sa.Column('ionization_energy', sa.Float(), nullable=True, comment='First ionization energy in kJ/mol.'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('atoms', 'ionization_energy')
