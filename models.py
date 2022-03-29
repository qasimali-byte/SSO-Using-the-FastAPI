from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100),nullable=False, unique=True )
    password = Column(String(100), nullable=False)
    username = Column(String(1000))

class UserSession(Base):
    __tablename__ = "users_session"
    id = Column(Integer, primary_key=True, index=True)
    cookie_id = Column(String(100),nullable=False, unique=True )
    user_id = Column(String(100), nullable=False, unique=True )