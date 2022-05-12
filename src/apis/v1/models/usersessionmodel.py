from sqlalchemy import Column, Integer, String
from . import Base
from sqlalchemy.dialects.postgresql import UUID

class UserSession(Base):
    __tablename__ = "users_session"
    id = Column(Integer, primary_key=True, index=True)
    cookie_id = Column(UUID(as_uuid=True),nullable=False, unique=True )
    user_id = Column(String(100), nullable=False, unique=True )