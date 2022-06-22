"""changing unique contraint in uuid

Revision ID: b1ee1c9c729b
Revises: 910e344dc956
Create Date: 2022-06-22 12:59:03.596229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1ee1c9c729b'
down_revision = '910e344dc956'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'idp_users', ['uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'idp_users', type_='unique')
    # ### end Alembic commands ###