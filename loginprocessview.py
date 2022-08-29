from fastapi import HTTPException
import json
from src.apis.v1.constants.sp_application_enums import SpAppsEnum
from src.apis.v1.routes import practices_routes
from src.apis.v1.services.roles_service import RolesService
from src.apis.v1.services.sps_service import SPSService
from src.apis.v1.services.user_service import UserService
from src.apis.v1.validators.sps_validator import SpAppsGeneralValidator
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
    def __init__(self) -> None:
        self.idp_server = server.Server(config_file="idp/idp_conf.py")

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

    def get_user_info(self, email,db: Session):
        user_info_data = UserService(db).get_user_info_db(email)
        users_info = dict({
            "username": user_info_data.username,
            "email": user_info_data.email,
            "first_name": user_info_data.first_name,
            "last_name": user_info_data.last_name


        })
        return users_info, user_info_data.id

    def get_sp_name(self, resp_args):
        try:
            print(resp_args["sp_entity_id"],"resp_args",SpAppsEnum(resp_args["sp_entity_id"]).name)
            return SpAppsEnum(resp_args["sp_entity_id"]).name
        except Exception as e:
            print(e,"error")
            raise HTTPException(status_code=500, detail="invalid sp_entity_id")

    def query_sp_apps_sp_metadata_name(self, sp_name, db: Session):
        sps_object = SPSService(db).get_sps_app_by_filter(sp_metadata=sp_name)
        if sps_object:
            return SpAppsGeneralValidator.from_orm(sps_object[0])
        else:
            raise HTTPException(status_code=500, detail="NO SP APP FOUND")

    def get(self, request_parms, email,db: Session):
        from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED, NameID, NAMEID_FORMAT_TRANSIENT

        saml_msg =request_parms
        data = self.idp_server.parse_authn_request(saml_msg,BINDING_HTTP_REDIRECT)
        verify_request_signature(data)
        resp_args = self.idp_server.response_args(data.message)
        sp_metadata_name = self.get_sp_name(resp_args)

        ## return the sp apps data
        sp_apps_data = self.query_sp_apps_sp_metadata_name(sp_metadata_name,db)
        practice_roles_data,practice_roles_status = UserService(db).get_all_sps_practice_roles_db(email)

        users_info, user_info_data_id = self.get_user_info(email,db)

        app_role=RolesService(db).get_user_selected_role_db_appid_userid(sp_apps_data.id,user_info_data_id )
        apps = list()

        for i in range(len(practice_roles_data)):
            if practice_roles_data[i].get('name') == str(sp_apps_data.name):
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
                try:
                    temp_list.append(app_role[1].name)
                except Exception as e:
                    temp_list.append(None)
                app_practices.append(str(temp_list))
                temp_list = list([])
        
        users_info['app_practices']=app_practices
        new_json_data = json.dumps(users_info)
        json_updated_data = json.loads(new_json_data.replace(r"\'", '"'))
        users_info["email"] = email
        identity = json_updated_data


        nid = NameID(name_qualifier="foo", format=NAMEID_FORMAT_TRANSIENT,
             text=email)
        value = self.idp_server.create_authn_response(identity,name_id=nid,userid=email,encrypt_cert_assertion=None,**resp_args)
        
        http_args = self.idp_server.apply_binding(
            binding=resp_args['binding'],
            msg_str=value,
            destination=resp_args['destination'],
            relay_state="/whoami",
            response=True)

        html_response = {
            "data": http_args,
            "type": "REDIRECT",
        }
        return html_response, resp_args