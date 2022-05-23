from . import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean
user_idp_sp_app = Table('user_idp_sp_app', Base.metadata,
    Column('idp_users_id', ForeignKey('idp_users.id')),
    Column('sp_apps_id', ForeignKey('sp_apps.id')),
    Column('is_accessible', Boolean, nullable=False, unique=False, default=True),
)
