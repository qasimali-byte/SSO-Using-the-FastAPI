from . import Base
from sqlalchemy import Column, Integer, ForeignKey

class sp_apps_role_driq_practice_role(Base):
    __tablename__ = "sp_apps_role_driq_practice_role"
    id = Column(Integer, primary_key=True)
    sp_apps_role_id = Column(ForeignKey('sp_apps_role.id'))
    driq_practices_role_id = Column(ForeignKey('driq_practices_role.id'))