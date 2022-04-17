from sqlalchemy.orm import Session
from models import Sps

class SPSController():
    def __init__(self, db: Session):
        self.db = db
    
    def get(self):
        return self.db.query(Sps).all()