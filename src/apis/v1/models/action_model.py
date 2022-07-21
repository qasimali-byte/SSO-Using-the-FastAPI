from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class action(Base):
    __tablename__ = "action"
    id = Column(Integer, primary_key=True)
    name = Column(String(255),nullable=True, unique=False)
    label = Column(String(255),nullable=True, unique=False)
    level = Column(String(155),nullable=True, unique=False)
    api = relationship("api", secondary="action_api", back_populates="action")