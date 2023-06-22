from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from . import Base
from src.apis.v1.models.sp_apps_model import SPAPPS
from src.apis.v1.models.practice_regions_model import practice_regions 

class practices(Base):
    __tablename__ = "practices"
    id = Column(Integer, primary_key=True)
    name = Column(String(255),nullable=False, unique=False)
    sp_apps_id = Column(Integer,ForeignKey('sp_apps.id'))
    practice_region_id = Column(Integer,ForeignKey('practices.id'))
    region_id = Column(Integer, ForeignKey('practice_regions.id')) 
    dr_iq_practice_id = Column(Integer, nullable=True)