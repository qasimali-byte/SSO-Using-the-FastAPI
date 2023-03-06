from . import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from src.apis.v1.models.sp_apps_role_model import sp_apps_role
# from src.apis.v1.models.idp_users_model import idp_users


class SPAPPS(Base):
    __tablename__ = "sp_apps"
    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String(255),nullable=True, unique=True)
    name = Column(String(100),nullable=False, unique=True)
    info = Column(String(100), nullable=True)
    host = Column(String(100), nullable=True)
    sp_metadata = Column(String(100),nullable=False, unique=True)
    logo_url = Column(String(255),nullable=True, unique=False)
    inactive_logo_url = Column(String(255),nullable=True, unique=False)
    is_active = Column(Boolean, nullable=False, unique=False, default=True)
    created_date = Column(DateTime, nullable=False, unique=False)
    updated_date = Column(DateTime, nullable=False, unique=False)
    email_verification_url = Column(String(255),nullable=True, unique=False)
    migration_url = Column(String(255),nullable=True, unique=False)
    roles = relationship("roles", secondary="sp_apps_role", back_populates='sp_apps')
    # idp_users=relationship("idp_users", secondary="idp_sp", back_populates='SPAPPS')
    
# from sqlalchemy.orm import joinedload

# requested_sp_apps = (
#     session.query(idp_users.email, SPAPPS.name, SPAPPS.id, idp_sp.requested_date)
#     .join(idp_sp, idp_users.id == idp_sp.idp_users_id)
#     .join(SPAPPS, idp_sp.sp_apps_id == SPAPPS.id)
#     .options(joinedload(idp_sp.idp_users), joinedload(idp_sp.sp_apps))
#     .filter(idp_sp.is_requested == True)
#     .all()
# )