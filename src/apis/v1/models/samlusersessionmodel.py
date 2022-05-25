from sqlalchemy import Column, Integer, String
from . import Base
from sqlalchemy.dialects.postgresql import UUID

class SAMLUserSession(Base):
    __tablename__ = "saml_users_session"
    id = Column(Integer, primary_key=True, index=True)
    cookie_id = Column(UUID(as_uuid=True),nullable=False, unique=True )
    saml_req = Column(String(500), nullable=False, unique=False )