from storesession import StoreSession
from utils import repr_saml, unpack_redirect, verify_request_signature
from saml2 import server
from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    entity,
)
from src.apis.v1.models import UserSession,User
from sqlalchemy.orm import Session

class LoginProcessView():
    def verify(self):
        verify_request_signature(data)

    def store_session(self, session_id, email,db: Session):
        store = StoreSession(db)
        if user_cookie := store.get_userid(email):
            store.delete(user_cookie)

        if not store.get(session_id):
            store.set(session_id, email)
            return "stored session"
        return "stored user session"

    def get_userid(self, session_id, db: Session):
        store = StoreSession(db)
        usersession_obj = store.get(session_id)
        if usersession_obj :
            return usersession_obj.user_id
        return None

    def get_session(self, session_id, db: Session):
        store = StoreSession(db)
        if type(session_id) == str:
            return "session not found"
        if store.get(session_id):
            return "session found"
        return "session not found"

    def get_user(self, email,password, db: Session):
        user = db.query(User).filter(User.email == email).first()
        if user :
            if user.password == password:
                return user
        
            return None
        return None

    def get(self, request_parms, email):
        from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED, NameID, NAMEID_FORMAT_TRANSIENT
        users_info = {
            "name": email,
            "email": email,
        }
        idp_server = server.Server(config_file="idp/idp_conf.py")
        # saml_msg = unpack_redirect(request_parms)
        saml_msg =request_parms
        data = idp_server.parse_authn_request(saml_msg,BINDING_HTTP_REDIRECT)
        verify_request_signature(data)
        users_info["email"] = email
        identity = users_info
        resp_args = idp_server.response_args(data.message)
        nid = NameID(name_qualifier="foo", format=NAMEID_FORMAT_TRANSIENT,
             text=email)
        value = idp_server.create_authn_response(identity,name_id=nid,userid=email,encrypt_cert_assertion=None,**resp_args)
        
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