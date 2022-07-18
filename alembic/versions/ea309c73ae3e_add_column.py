"""add column

Revision ID: ea309c73ae3e
Revises: 3e4bffe113d9
Create Date: 2022-07-14 19:35:50.118985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea309c73ae3e'
down_revision = '3e4bffe113d9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users',sa.Column('phone',sa.Integer(),nullable=False))
    pass


def downgrade():
    op.drop_column('users','phone')
    pass
