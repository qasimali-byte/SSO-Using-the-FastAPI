from . import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean

class idp_user_role(Base):
    __tablename__ = "idp_user_role"
    id = Column(Integer, primary_key=True)
    idp_users_id = Column(ForeignKey('idp_users.id'))
    roles_id = Column(ForeignKey('roles.id'))
    