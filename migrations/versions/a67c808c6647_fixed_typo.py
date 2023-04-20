"""Fixed typo

Revision ID: a67c808c6647
Revises: 45016b1511cc
Create Date: 2023-04-18 13:35:51.008786

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "a67c808c6647"
down_revision = "45016b1511cc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
