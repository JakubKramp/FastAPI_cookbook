"""Removed DRI model

Revision ID: ed922a71ba88
Revises: 7e72dbe92283
Create Date: 2023-04-26 12:40:55.810964

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ed922a71ba88"
down_revision = "7e72dbe92283"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "profile",
        "sex",
        existing_type=postgresql.ENUM("male", "female", name="sex"),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "profile",
        "sex",
        existing_type=postgresql.ENUM("male", "female", name="sex"),
        nullable=True,
    )
    # ### end Alembic commands ###
