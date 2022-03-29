from utils import repr_saml, unpack_redirect, verify_request_signature
from saml2 import server
from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    entity,
)
from idp_user import USERS
from models import User
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

class Store(ABC):
    """Abstract class that defines methods for interacting with session data. """
    
    @abstractmethod
    def get(self, key):
        raise NotImplementedError()
    
    @abstractmethod
    def set(self, key, value):
        raise NotImplementedError()
    
    @abstractmethod
    def delete(self, key):
        raise NotImplementedError()

class StoreSession(Store):
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, key):
        return self.db.query(User).filter_by(email=key).first()
    
    def set(self, key, value):
        self.db.add(value)
        self.db.commit()
    
    def delete(self, key):
        self.db.query(User).filter_by(email=key).delete()
        self.db.commit()

class LoginProcessView():
    def verify(self):
        verify_request_signature(data)

    def store_session(self, session_id, email,db: Session):
        pass

    def get_user(self, email,password, db: Session):
        user = db.query(User).filter(User.email == email).first()
        if user :
            if user.password == password:
                return user
        
            return None
        return None

    def get(self, request_parms):
        idp_server = server.Server(config_file="./idp_conf.py")
        # saml_msg = unpack_redirect(request_parms)
        saml_msg =request_parms
        print(saml_msg)
        data = idp_server.parse_authn_request(saml_msg,BINDING_HTTP_REDIRECT)
        verify_request_signature(data)
        identity = USERS["testuser"].copy()
        resp_args = idp_server.response_args(data.message)
        value = idp_server.create_authn_response(identity,userid="testuser",encrypt_cert_assertion=None,**resp_args)
        
        http_args = idp_server.apply_binding(
            binding=resp_args['binding'],
            msg_str=value,
            destination=resp_args['destination'],
            relay_state="/whoami",
            response=True)

        html_response = {
            "data": http_args,
            "type": "REDIRECT",
        }
        return html_response