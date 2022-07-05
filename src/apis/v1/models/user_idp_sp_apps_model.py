from . import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.apis.v1.models.sp_apps_model import SPAPPS



class idp_sp(Base):
    __tablename__ = "idp_sp"
    id = Column(Integer, primary_key=True)
    idp_users_id = Column(ForeignKey('idp_users.id'))
    sp_apps_id = Column(ForeignKey('sp_apps.id'))
    is_accessible = Column(Boolean, nullable=False, unique=False, default=True)
