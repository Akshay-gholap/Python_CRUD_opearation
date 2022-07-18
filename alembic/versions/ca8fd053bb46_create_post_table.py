"""create post table

Revision ID: ca8fd053bb46
Revises: 
Create Date: 2022-07-14 18:34:50.747184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca8fd053bb46'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False))
    pass 

def downgrade() -> None:
    op.drop_table('posts')
    pass 
