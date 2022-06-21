from sqlalchemy import Column, Integer, String
from . import Base

class gender(Base):
    __tablename__ = "gender"
    id = Column(Integer, primary_key=True)
    name = Column(String(255),nullable=False)