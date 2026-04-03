"""shorturl_table

Revision ID: 160f70db8571
Revises: 
Create Date: 2026-04-03 11:30:16.259089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '160f70db8571'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("shorturls",
                    sa.Column("id", sa.Integer, primary_key=True, index=True),
                    sa.Column("original_url", sa.String, nullable=False),
                    sa.Column("short_code", sa.String, unique=True, nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table("shorturls")  
    pass
