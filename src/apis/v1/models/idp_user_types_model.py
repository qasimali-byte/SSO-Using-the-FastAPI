from sqlalchemy import Column, DateTime, Integer, String
from . import Base

class idp_user_types(Base):
    __tablename__ = "idp_user_types"
    id = Column(Integer, primary_key=True)
    user_type = Column(String(255),nullable=False)
    created_date = Column(DateTime, nullable=False, unique=False)
    updated_date = Column(DateTime, nullable=False, unique=False)