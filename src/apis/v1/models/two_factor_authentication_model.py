from . import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID


class two_factor_authentication(Base):
    __tablename__ = "two_factor_authentication"
    id = Column(Integer, primary_key=True, index=True)
    cookie_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    user_id = Column(String(100), nullable=False, unique=True)
