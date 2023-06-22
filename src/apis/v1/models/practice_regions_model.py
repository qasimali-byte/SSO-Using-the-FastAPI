from sqlalchemy import Column,  Integer, String 
from . import Base

class practice_regions(Base):
    __tablename__ = "practice_regions"
    id = Column(Integer, primary_key=True)
    name = Column(String(255),nullable=False, unique=False)
