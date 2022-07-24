from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class api(Base):
    __tablename__ = "api"
    id = Column(Integer, primary_key=True)
    name = Column(String(255),nullable=True, unique=False)
    label = Column(String(255),nullable=True, unique=False)
    method = Column(String(255),nullable=True, unique=False)
    action = relationship("action", secondary="action_api", back_populates="api")