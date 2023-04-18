"""Fixed typo

Revision ID: bd73a0ad0266
Revises: a67c808c6647
Create Date: 2023-04-18 13:38:10.707369

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "bd73a0ad0266"
down_revision = "a67c808c6647"
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
