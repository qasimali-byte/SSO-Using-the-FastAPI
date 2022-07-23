import json
from src.apis.v1.routes import practices_routes
from src.apis.v1.services.roles_service import RolesService
from src.apis.v1.services.user_service import UserService
from storesession import StoreSession
from utils import repr_saml, unpack_redirect, verify_request_signature
from saml2 import server
from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    entity,
)
from src.apis.v1.models import UserSession,idp_users,User
from sqlalchemy.orm import Session
from src.apis.v1.controllers.auth_controller import AuthController

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
        user = db.query(idp_users).filter(idp_users.email == email).first()        
        if user :
            var=AuthController(db).login_authentication(user.email, password)
            if var[1]==200:
                return user
            return None
        return None

    def get(self, request_parms, email,db: Session):
        from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED, NameID, NAMEID_FORMAT_TRANSIENT
        user_info_data = UserService(db).get_user_info_db(email)
        practice_roles_data,practice_roles_status=UserService(db).get_all_sps_practice_roles_db(email)
        users_info = dict({
            "username": user_info_data.username,
            "email": user_info_data.email,
            "first_name": user_info_data.first_name,
            "last_name": user_info_data.last_name


        })

        app_role=RolesService(db).get_user_selected_role_db_appid_userid(4,user_info_data.id)
        apps = list()

        for i in range(len(practice_roles_data)):
            if practice_roles_data[i].get('name') == 'ez-analytics':
                apps.append({'app_practices': practice_roles_data[i].get('practices')})
        
        app_practices_list = list()
        for app in apps[0]['app_practices']:
            try:
                app_practices_list.append({'parent': app['name'], 'practices': app['practices']})
            except:
                pass
        app_practices = list([])
        for i in range(len(app_practices_list)):
            temp_list = list([])
            for index in range(len(app_practices_list[i]['practices'])):
                temp_list.append(app_practices_list[i]['parent'])
                temp_list.append(app_practices_list[i]['practices'][index]['name'])
                temp_list.append(app_role[1].name)
                app_practices.append(str(temp_list))
                temp_list = list([])
        
        users_info['app_practices']=app_practices
        new_json_data = json.dumps(users_info)
        json_updated_data = json.loads(new_json_data.replace(r"\'", '"'))
        print('json_updated_data---',json_updated_data)
        idp_server = server.Server(config_file="idp/idp_conf.py")
        # saml_msg = unpack_redirect(request_parms)
        saml_msg =request_parms
        data = idp_server.parse_authn_request(saml_msg,BINDING_HTTP_REDIRECT)
        verify_request_signature(data)
        users_info["email"] = email
        identity = json_updated_data
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