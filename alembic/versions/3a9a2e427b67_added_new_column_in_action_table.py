"""added new column in action table

Revision ID: 3a9a2e427b67
Revises: b1ee1c9c729b
Create Date: 2022-07-14 14:37:22.669556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a9a2e427b67'
down_revision = 'b1ee1c9c729b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('action',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('name', sa.String(length=255), nullable=True),
    # sa.Column('label', sa.String(length=255), nullable=True),
    # sa.PrimaryKeyConstraint('id')
    # )
    # op.create_table('user_action',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('idp_user_id', sa.Integer(), nullable=True),
    # sa.Column('action_id', sa.Integer(), nullable=True),
    # sa.Column('role_id', sa.Integer(), nullable=True),
    # sa.Column('action_level', sa.String(length=155), nullable=False),
    # sa.Column('action_date', sa.DateTime(), nullable=False),
    # sa.Column('status', sa.String(length=255), nullable=False),
    # sa.ForeignKeyConstraint(['action_id'], ['action.id'], ),
    # sa.ForeignKeyConstraint(['idp_user_id'], ['idp_users.id'], ),
    # sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    # sa.PrimaryKeyConstraint('id')
    # )
    op.drop_table('user_idp_sp_app')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_idp_sp_app',
    sa.Column('idp_users_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('sp_apps_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('is_accessible', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['idp_users_id'], ['idp_users.id'], name='user_idp_sp_app_idp_users_id_fkey'),
    sa.ForeignKeyConstraint(['sp_apps_id'], ['sp_apps.id'], name='user_idp_sp_app_sp_apps_id_fkey')
    )
    op.drop_table('user_action')
    op.drop_table('action')
    # ### end Alembic commands ###
