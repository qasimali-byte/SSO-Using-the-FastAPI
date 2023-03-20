from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from src.apis.v1.models import UserSession

class Store(ABC):
    """Abstract class that defines methods for interacting with session data. """
    
    @abstractmethod
    def get(self, key):
        raise NotImplementedError()
    
    @abstractmethod
    def get_userid(self, key):
        raise NotImplementedError()

    @abstractmethod
    def set(self, cookieid, userid):
        raise NotImplementedError()
    
    @abstractmethod
    def delete(self, key):
        raise NotImplementedError()

class StoreSession(Store):
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, key):
        print('storesession.py file ', key)
        return self.db.query(UserSession).filter_by(cookie_id=key).first()
    
    def get_userid(self,key):
        return self.db.query(UserSession).filter_by(user_id=key).first()

    def set(self, cookieid, userid):
        user_session = UserSession(cookie_id=cookieid, user_id=userid)
        self.db.add(user_session)
        self.db.commit()
        return "stored user session"
    
    def delete(self, key):
        # user_session = self.get_userid(key)
        self.db.delete(key)
        self.db.commit()
        return "deleted user session"

