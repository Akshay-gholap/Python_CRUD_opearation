"""add new content column

Revision ID: 4f7f1db15cf6
Revises: ca8fd053bb46
Create Date: 2022-07-14 18:49:06.827016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f7f1db15cf6'
down_revision = 'ca8fd053bb46'
branch_labels = None
depends_on = None


def upgrade() :
    op.add_column('posts',sa.Column('content', sa.String(),nullable=False))
    pass 


def downgrade() :
    op.drop_column('posts', 'content')
    pass
