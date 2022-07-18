"""creating user table

Revision ID: 28903eada7d9
Revises: 4f7f1db15cf6
Create Date: 2022-07-14 19:23:00.055065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28903eada7d9'
down_revision = '4f7f1db15cf6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('email', sa.String(), nullable=False, unique=True))
    pass


def downgrade():
    op.drop_table('users')
    pass
