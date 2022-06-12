from . import Base
from sqlalchemy import Column, Integer, ForeignKey

class type_role_permissions(Base):
    __tablename__ = "type_role_permissions"
    id = Column(Integer, primary_key=True)
    type_id = Column(ForeignKey('idp_user_types.id'))
    roles_id = Column(ForeignKey('roles.id'))
    permissions_id = Column(ForeignKey('permissions.id'))