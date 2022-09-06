from . import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean

class role_api(Base):
    __tablename__ = "role_api"
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer,ForeignKey('roles.id'))
    api_id = Column(ForeignKey('api.id'))
    is_allowed = Column(Boolean, nullable=True, unique=False, default=True)