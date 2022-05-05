from sqlalchemy.orm import Session
from src.apis.v1.models import Sps

class SPSController():
    def __init__(self, db: Session):
        self.db = db
    
    def get(self):
        return self.db.query(Sps).all()