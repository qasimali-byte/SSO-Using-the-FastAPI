from . import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class sp_apps_role(Base):
    __tablename__ = "sp_apps_role"
    id = Column(Integer, primary_key=True)
    sp_apps_id = Column(ForeignKey('sp_apps.id'))
    roles_id = Column(ForeignKey('roles.id'))
    driq_practices_role = relationship("driq_practices_role", secondary="sp_apps_role_driq_practice_role", back_populates='sp_apps_role')
    idp_users = relationship("idp_users", secondary="idp_user_apps_roles", back_populates='sp_apps_role')