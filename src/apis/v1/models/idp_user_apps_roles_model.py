from . import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class idp_user_apps_roles(Base):
    __tablename__ = "idp_user_apps_roles"
    id = Column(Integer, primary_key=True)
    idp_users_id = Column(ForeignKey('idp_users.id'))
    sp_apps_role_id = Column(ForeignKey('sp_apps_role.id'))
    sub_roles_id = Column(ForeignKey('driq_practices_role.id'))