from . import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
user_idp_sp_app_table = Table('user_idp_sp_app', Base.metadata,
    Column('idp_users_id', ForeignKey('idp_users.id')),
    Column('sp_apps_id', ForeignKey('sp_apps.id'))
)
