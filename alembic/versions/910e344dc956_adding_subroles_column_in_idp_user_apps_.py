"""adding subroles column in idp_user_apps_roles

Revision ID: 910e344dc956
Revises: 9e3d49200697
Create Date: 2022-06-20 15:26:02.289453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '910e344dc956'
down_revision = '9e3d49200697'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('idp_user_role')
    op.add_column('idp_user_apps_roles', sa.Column('sub_roles_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'idp_user_apps_roles', 'driq_practices_role', ['sub_roles_id'], ['id'])
    op.create_foreign_key(None, 'idp_users', 'gender', ['dr_iq_gender_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'idp_users', type_='foreignkey')
    op.drop_constraint(None, 'idp_user_apps_roles', type_='foreignkey')
    op.drop_column('idp_user_apps_roles', 'sub_roles_id')
    op.create_table('idp_user_role',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('idp_users_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('roles_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['idp_users_id'], ['idp_users.id'], name='idp_user_role_idp_users_id_fkey'),
    sa.ForeignKeyConstraint(['roles_id'], ['roles.id'], name='idp_user_role_roles_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='idp_user_role_pkey')
    )
    # ### end Alembic commands ###
