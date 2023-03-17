from abc import abstractmethod
from ctypes import Union
from typing import Generic
from uuid import UUID, uuid4
from fastapi import HTTPException
from itsdangerous import BadSignature, SignatureExpired
from sqlalchemy.orm import Session
from fastapi_sessions.backends.session_backend import SessionBackend, SessionModel

from fastapi_sessions.frontends.session_frontend import ID, FrontendError, SessionFrontend
try:
    from src.apis.v1.models import UserSession
    from serializers import SessionSerializer
except ImportError:
    from serializers import SessionSerializer

from abc import ABC, abstractmethod

class Store(ABC):
    """Abstract class that defines methods for interacting with session data. """

    @abstractmethod
    def get(self, filter_key: str, filter_value: str) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def set(self, cookieid, userid):
        raise NotImplementedError()
    
    @abstractmethod
    def delete(self, filter_key: str, filter_value: str):
        raise NotImplementedError()


class SessionStore(Store):
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, filter_key: str, filter_value: str):
        if filter_key == "user_id":
            return self.db.query(UserSession).filter_by(user_id=filter_value).first()
        elif filter_key == "cookie_id":
            return self.db.query(UserSession).filter_by(cookie_id=filter_value).first()
        else:
            return "Invalid filter key"

    def set(self, cookieid, userid):
        primary_id = 0
        user_check = self.get("user_id", userid)
        if user_check:
            return "User already has a session"
        
        ### reset the id if the user session gets deleted ###
        if id_:= self.db.query(UserSession).order_by(UserSession.id.desc()).first():
            primary_id = id_.id + 1

        user_session = UserSession(id=primary_id,cookie_id=cookieid, user_id=userid)
        self.db.add(user_session)
        self.db.commit()
        return "stored user session"
    
    def delete(self, filter_key: str, filter_value: str):
        user_delete = self.get(filter_key, filter_value)
        self.db.delete(user_delete)
        self.db.commit()
        return "deleted user session"

    def update(self, filter_key: str, filter_value: str, update_key: str, update_value):
        user_update = self.get(filter_key, filter_value)
        setattr(user_update, update_key, update_value)
        self.db.commit()
        return "updated user session"

class SessionVerfication():

    @staticmethod
    def verify_cookie(cookie,request):
        signed_session_id = request.cookies.get(cookie.model.name)

class SessionController(Generic[ID, SessionModel]):

    @property
    @abstractmethod
    def identifier(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def backend(self) -> SessionBackend[ID, SessionModel]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def auto_error(self) -> bool:
        raise NotImplementedError()

    @property
    @abstractmethod
    def auth_http_exception(self) -> HTTPException:
        raise NotImplementedError()

    @abstractmethod
    def verify_session(self, model: SessionModel) -> bool:
        raise NotImplementedError()
        
    @staticmethod
    def serialize_usersession(cookie_id,user_id):
        try:
            return SessionSerializer(cookie_id=cookie_id,user_id=user_id),True
        except Exception as e:
            return "Error: {}".format(e), False

    @staticmethod
    def check_session_db(db, cookie_id):
        print('check_session_db function')
        try:
            session_ = SessionStore(db)
            if session_.get("cookie_id",cookie_id):
                return "Session found", 200
            return "Session not found", 404
        except Exception as e:
            return "Error: {}".format(e), 500

    @staticmethod
    def check_session_redis(sessionStorage, cookie_id):
        try:

            if sessionStorage[cookie_id]:
                return "Session found", 200
            return "Session not found", 404
        except Exception as e:
            return "Error: {}".format(e), 500

    @staticmethod
    def verify_session(cookie,request):
        print('verifying session functionality')
        try:
            signed_session_id = request.cookies.get(cookie.model.name)
            if not signed_session_id:
                if cookie.auto_error:
                    return "No session provided", 403
                return "No session cookie attached to request", 403
                    # Verify and timestamp the signed session id
            try:
                session_id = UUID(
                    cookie.signer.loads(
                        signed_session_id,
                        max_age=cookie.cookie_params.max_age,
                        return_timestamp=False,
                    )
                )
            except (SignatureExpired, BadSignature):
                if cookie.auto_error:
                    return "Invalid session provided", 403
                    
                return "Session cookie has invalid signature", 403

            """Attach the extracted session id to the request."""
            try:
                request.state.session_ids[cookie.identifier] = session_id
            except Exception:
                request.state.session_ids = {}
                request.state.session_ids[cookie.identifier] = session_id

            try:
                identifier = cookie.identifier
                print(identifier)
                session_id: Union[ID, FrontendError] = request.state.session_ids[
                    identifier
                ]
            except:
                if cookie.auto_error:
                    return "internal failure of session verification", 403

                else:
                    return "failed to extract the {} session from state", 403
            
            return session_id, 200

        except Exception as e:
            print("--- Error: {}".format(str(e)))
    
    @staticmethod
    def check_userid(user_id):
        try:
            return Store.check_userid(user_id)
        except Exception as e:
            return "Error: {}".format(e), 500

    @staticmethod
    def get_userid(db:Session, cookie_id):
        try:
            session_ = SessionStore(db)
            return session_.get("cookie_id",cookie_id).user_id, 200
        except Exception as e:
            return "Error: {}".format(e), 404

    @staticmethod
    def delete_session(db:Session, cookie_id):
        try:
            session_ = SessionStore(db)
            return session_.delete("cookie_id",cookie_id), 200
        except Exception as e:
            return "Error: {}".format(e), 500
    
    @staticmethod
    def delete_userid(db:Session, user_id):
        try:
            session_ = SessionStore(db)
            return session_.delete("user_id",user_id), 200
        except Exception as e:
            return "Error: {}".format(e), 500

    @staticmethod
    def create_session(db: Session, user_id: str, cookie, response):
        session_id = uuid4()
        valid_ = SessionController().serialize_usersession(session_id,user_id)
        session_ = SessionStore(db)
        ## if user_id exsists in db update session
        if valid_[1] == True:
            if session_.get("user_id",user_id):
                # update session
                session_.update("user_id",user_id,"cookie_id",session_id)
            else:
                # create session
                session_.set(session_id,user_id)
        elif valid_[1] == False:
            return valid_[0], 500

        # set cookie
        cookie.attach_to_response(response, session_id)
        return response
        # primary_id = 0
        # if id_:= db.query(UserSession).order_by(UserSession.id.desc()).first():
        #     primary_id = id_.id + 1
        # user_session = UserSession(id=primary_id,cookie_id=cookie_id, user_id=user_id)
        # db.add(user_session)
        # db.commit()
        # return user_session


