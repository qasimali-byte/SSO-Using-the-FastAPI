"""updated column role_name in user_action_model

Revision ID: 4aee501c27fb
Revises: 842e366cac94
Create Date: 2022-07-16 15:00:56.387050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4aee501c27fb'
down_revision = '842e366cac94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_action', 'role_name',
               existing_type=sa.VARCHAR(length=155),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_action', 'role_name',
               existing_type=sa.VARCHAR(length=155),
               nullable=False)
    # ### end Alembic commands ###
