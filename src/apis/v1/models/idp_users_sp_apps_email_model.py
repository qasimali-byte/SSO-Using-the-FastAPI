from . import Base
from sqlalchemy import Column,Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.apis.v1.models.sp_apps_model import SPAPPS
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.models.serviceprovidersmodel import Sps


class idp_users_sp_apps_email(Base):
    '''
    This is the association table to make the relationship of primary email to other sp apps email
    '''
    __tablename__ = "idp_users_sp_apps_email"
    id = Column(Integer, primary_key=True)
    idp_users_id = Column(ForeignKey('idp_users.id'))
    sp_apps_id = Column(ForeignKey('sp_apps.id'))
    primary_email=Column(String(100),nullable=True, unique=False)
    sp_apps_email=Column(String(100),nullable=True, unique=False)
    sp_apps_name=Column(String(100),nullable=True, unique=False)