from sqlalchemy import Column, Integer, String
from . import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100),nullable=False, unique=True)
    password = Column(String(155), nullable=False)
    username = Column(String(1000))