"""changing sp application roles relation from one to many to many

Revision ID: 3c14414858ca
Revises: d1eef53fe6c7
Create Date: 2022-06-14 18:00:13.534586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c14414858ca'
down_revision = 'd1eef53fe6c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_constraint('roles_sp_apps_id_fkey', 'roles', type_='foreignkey')
    # op.drop_column('roles', 'sp_apps_id')
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('sp_apps_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('roles_sp_apps_id_fkey', 'roles', 'sp_apps', ['sp_apps_id'], ['id'])
    # ### end Alembic commands ###
