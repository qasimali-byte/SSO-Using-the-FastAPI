from sqlalchemy import Column, Integer, String, Boolean, DateTime
from . import Base

class SPAPPS(Base):
    __tablename__ = "sp_apps"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100),nullable=False, unique=True)
    info = Column(String(100), nullable=True)
    host = Column(String(100), nullable=True)
    sp_metadata = Column(String(100),nullable=False, unique=True)
    logo_url = Column(String(255),nullable=True, unique=False)
    is_active = Column(Boolean, nullable=False, unique=False, default=True)
    created_date = Column(DateTime, nullable=False, unique=False)
    updated_date = Column(DateTime, nullable=False, unique=False)