from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from . import Base

class practices(Base):
    __tablename__ = "practices"
    id = Column(Integer, primary_key=True)
    name = Column(String(255),nullable=False, unique=False)
    sp_apps_id = Column(Integer,ForeignKey('sp_apps.id'))