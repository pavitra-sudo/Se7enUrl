"""click count

Revision ID: e1d9b5efe7dd
Revises: 160f70db8571
Create Date: 2026-04-03 20:19:18.494493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1d9b5efe7dd'
down_revision: Union[str, Sequence[str], None] = '160f70db8571'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("shorturls", sa.Column("click_count", sa.Integer, default=0))



def downgrade() -> None:
    op.drop_column("shorturls", "click_count")
    
