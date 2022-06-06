from xmlrpc.client import Boolean
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.apis.v1.models.idp_user_types_model import idp_user_types
from . import Base

class roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(255),nullable=False, unique=True)
    label = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, unique=False, default=True)
    user_type_id = Column(Integer, ForeignKey("idp_user_types.id"))
    # user_type = relationship("idp_user_types", backref="roles", lazy="joined")