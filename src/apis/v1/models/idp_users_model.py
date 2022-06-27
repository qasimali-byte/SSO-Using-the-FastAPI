from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from . import Base
# from src.apis.v1.models.user_idp_sp_apps_model import idp_sp, user_idp_sp_app

class idp_users(Base):
    __tablename__ = "idp_users"
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True),nullable=False, unique=True )
    organization_id = Column(String(100),nullable=False, unique=False)
    username = Column(String(100),nullable=False, unique=False)
    title = Column(String(100),nullable=True, unique=False)
    first_name = Column(String(100),nullable=False, unique=False)
    last_name = Column(String(100),nullable=False, unique=False)
    email = Column(String(100),nullable=False, unique=True)
    other_email = Column(String(100),nullable=True, unique=False)
    gender = Column(String(100),nullable=True, unique=False)
    nhs_number = Column(String(100),nullable=False, unique=False)
    password_hash = Column(String(255), nullable=False)
    reset_password_token = Column(String(255), nullable=False, unique=False)
    reset_password_token_expiry = Column(String(255), nullable=False, unique=False)
    profile_image = Column(String(255), nullable=True, unique=False)
    contact_no = Column(String(255), nullable=True, unique=False)
    address = Column(String(255), nullable=True, unique=False)
    is_approved = Column(Boolean, nullable=False, unique=False, default=False)
    is_rejected = Column(Boolean, nullable=False, unique=False, default=False)
    is_on_hold = Column(Boolean, nullable=False, unique=False, default=True)
    is_superuser = Column(Boolean, nullable=False, unique=False, default=False)
    is_active = Column(Boolean, nullable=False, unique=False, default=True)
    created_date = Column(DateTime, nullable=False, unique=False)
    updated_date = Column(DateTime, nullable=False, unique=False)
    last_login_date = Column(DateTime, nullable=True, unique=False)
    user_type_id = Column(Integer, ForeignKey("idp_user_types.id"))
    dr_iq_gender_id = Column(Integer, ForeignKey("gender.id"))
    sp_apps_role = relationship("sp_apps_role", secondary="idp_user_apps_roles", back_populates='idp_users')
    SPAPPS = relationship("SPAPPS", secondary="idp_sp", back_populates='idp_users')
    
    # user_type = relationship("idp_user_types", backref="idp_users")
    # idp_sp = relationship("idp_sp", lazy="joined")