from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100),nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    username = Column(String(1000))

class UserSession(Base):
    __tablename__ = "users_session"
    id = Column(Integer, primary_key=True, index=True)
    cookie_id = Column(UUID(as_uuid=True),nullable=False, unique=True )
    user_id = Column(String(100), nullable=False, unique=True )

class Sps(Base):
    __tablename__ = "service_providers"
    id = Column(Integer, primary_key=True, index=True)
    sp_id = Column(String(100),nullable=False, unique=True )