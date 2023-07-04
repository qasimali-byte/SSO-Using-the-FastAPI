from . import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.apis.v1.models.sp_apps_model import SPAPPS

class idp_users_practices(Base):
    __tablename__ = "idp_users_practices"
    id = Column(Integer, primary_key=True)
    idp_users_id = Column(ForeignKey('idp_users.id'))
    practices_id = Column(ForeignKey('practices.id'))
    dr_iq_practice_region_id = Column(ForeignKey('practice_regions.id'), nullable=True)

