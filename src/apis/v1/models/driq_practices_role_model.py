from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class driq_practices_role(Base):
    __tablename__ = "driq_practices_role"
    id = Column(Integer, primary_key=True)
    name = Column(String(255),nullable=False, unique=False)
    label = Column(String(255),nullable=False)
    dr_iq_practice_role_id = Column(Integer, nullable=True)
    sp_apps_role = relationship("sp_apps_role", secondary="sp_apps_role_driq_practice_role", back_populates='driq_practices_role')