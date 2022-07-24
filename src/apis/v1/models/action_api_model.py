from . import Base
from sqlalchemy import Column, Integer, ForeignKey

class action_api(Base):
    __tablename__ = "action_api"
    id = Column(Integer, primary_key=True)
    action_id = Column(Integer,ForeignKey('action.id'))
    api_id = Column(ForeignKey('api.id'))