from . import Base
from sqlalchemy import Column, DateTime,Integer, String, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.apis.v1.models.sp_apps_model import SPAPPS
import datetime


class idp_sp(Base):
    __tablename__ = "idp_sp"
    id = Column(Integer, primary_key=True)
    idp_users_id = Column(ForeignKey('idp_users.id'))
    sp_apps_id = Column(ForeignKey('sp_apps.id'))
    is_accessible = Column(Boolean, nullable=False)
    is_verified=Column(Boolean, nullable=True)
    is_requested=Column(Boolean, nullable=True)
    action_status=Column(Boolean, nullable=True)
    requested_email=Column(String(100),nullable=True, unique=False)
    requested_user_id=Column(String(100),nullable=True, unique=False)
    requested_date =  Column(DateTime, nullable=True, unique=False,default=datetime.datetime.utcnow())
    action_date = Column(DateTime, nullable=True, unique=False, default=datetime.datetime.utcnow())
    action=Column(String(100), nullable=True, unique=False)