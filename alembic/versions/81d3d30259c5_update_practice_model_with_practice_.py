"""update practice model with practice_region_id 

Revision ID: 81d3d30259c5
Revises: 61d0f23275fe
Create Date: 2022-06-13 16:18:53.374075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81d3d30259c5'
down_revision = '61d0f23275fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('practices', sa.Column('practice_region_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'practices', 'practices', ['practice_region_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'practices', type_='foreignkey')
    op.drop_column('practices', 'practice_region_id')
    # ### end Alembic commands ###
