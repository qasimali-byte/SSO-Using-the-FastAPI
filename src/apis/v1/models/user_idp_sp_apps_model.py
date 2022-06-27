from . import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.apis.v1.models.sp_apps_model import SPAPPS


user_idp_sp_app = Table('user_idp_sp_app', Base.metadata,
    Column('idp_users_id', ForeignKey('idp_users.id')),
    Column('sp_apps_id', ForeignKey('sp_apps.id')),
    Column('is_accessible', Boolean, nullable=False, unique=False, default=True),
)

class idp_sp(Base):
    __tablename__ = "idp_sp"
    id = Column(Integer, primary_key=True)
    idp_users_id = Column(ForeignKey('idp_users.id'))
    sp_apps_id = Column(ForeignKey('sp_apps.id'))
    is_accessible = Column(Boolean, nullable=False, unique=False, default=True)
    # sp_apps_table = relationship("SPAPPS", lazy="joined")