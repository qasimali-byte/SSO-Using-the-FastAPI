from src.apis.v1.models.sp_apps_model import SPAPPS
from . import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.apis.v1.models.idp_user_types_model import idp_user_types
from src.apis.v1.models.sp_apps_role_model import sp_apps_role

class roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(255),nullable=False, unique=True)
    label = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, unique=False, default=True)
    user_type_id = Column(Integer, ForeignKey("idp_user_types.id"))
    type_role_permissions = Column(Integer, ForeignKey("type_role_permissions.id"))
    sp_apps = relationship("SPAPPS", secondary="sp_apps_role", back_populates='roles')