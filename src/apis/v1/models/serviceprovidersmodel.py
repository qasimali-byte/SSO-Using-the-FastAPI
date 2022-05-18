from sqlalchemy import Column, Integer, String
from . import Base

class Sps(Base):
    __tablename__ = "service_providers"
    id = Column(Integer, primary_key=True, index=True)
    sp_id = Column(String(100),nullable=False, unique=True )
    sp_name = Column(String(100),nullable=True, unique=False, default="")