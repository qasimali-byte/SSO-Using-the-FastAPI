from email.policy import default
from xmlrpc.client import Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from . import Base

class idp_users(Base):
    __tablename__ = "idp_users"
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True),nullable=False, unique=True )
    organization_id = Column(String(100),nullable=False, unique=True)
    username = Column(String(100),nullable=False, unique=False)
    title = Column(String(100),nullable=True, unique=False)
    first_name = Column(String(100),nullable=False, unique=False)
    last_name = Column(String(100),nullable=False, unique=False)
    email = Column(String(100),nullable=False, unique=True)
    other_email = Column(String(100),nullable=False, unique=False)
    gender = Column(String(100),nullable=False, unique=False)
    nhs_number = Column(String(100),nullable=False, unique=False)
    password_hash = Column(String(255), nullable=False)
    reset_password_token = Column(String(255), nullable=False, unique=False)
    reset_password_token_expiry = Column(String(255), nullable=False, unique=False)
    profile_image = Column(String(255), nullable=True, unique=False)
    contact_no = Column(String(255), nullable=False, unique=False)
    address = Column(String(255), nullable=False, unique=False)
    is_approved = Column(Boolean, nullable=False, unique=False, default=False)
    is_rejected = Column(Boolean, nullable=False, unique=False, default=False)
    is_on_hold = Column(Boolean, nullable=False, unique=False, default=True)
    is_superuser = Column(Boolean, nullable=False, unique=False, default=False)
    is_active = Column(Boolean, nullable=False, unique=False, default=True)
    created_date = Column(DateTime, nullable=False, unique=False)
    updated_date = Column(DateTime, nullable=False, unique=False)
    last_login_date = Column(DateTime, nullable=False, unique=False)
    sp_apps_relation = relationship("Child",
                secondary=association_table)