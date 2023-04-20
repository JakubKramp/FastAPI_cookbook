"""Removed enum fields

Revision ID: 9bd8e7c8e008
Revises: 948c7c8f64f7
Create Date: 2023-04-20 14:57:43.137322

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9bd8e7c8e008'
down_revision = '948c7c8f64f7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profile', 'activity_factor')
    op.drop_column('profile', 'sex')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profile', sa.Column('sex', postgresql.ENUM('male', 'female', name='sex'), autoincrement=False, nullable=True))
    op.add_column('profile', sa.Column('activity_factor', postgresql.ENUM('little', 'one_time', 'two_times', 'three_times', 'every_day', 'professional_athlete', name='activityfactor'), autoincrement=False, nullable=True))
    # ### end Alembic commands ###