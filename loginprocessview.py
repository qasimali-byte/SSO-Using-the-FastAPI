from fastapi import HTTPException,status
import json
from src.apis.v1.constants.sp_application_enums import SpAppsEnum
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.helpers.filter_List_dictionaries import get_item
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
        self.sp_metadata_name:str = ""

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
            "last_name": user_info_data.last_name,
            "contact_no": user_info_data.contact_no


        })
        return users_info, user_info_data.id

    def get_sp_name(self, resp_args):
        try:
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

    def get_sp_apps_email(self,db:Session,sp_apps_id:int,primary_email:str):
        return SPSController(db).get_sp_apps_email(sp_apps_id,primary_email)
    
    def verify_app_allowed(self, request_parms, db: Session, user_email: str) -> bool:
        ## verifies whether is app allowed to the user or not
        saml_msg = request_parms
        data = self.idp_server.parse_authn_request(saml_msg,BINDING_HTTP_REDIRECT)
        verify_request_signature(data)
        resp_args = self.idp_server.response_args(data.message)
        sp_metadata_name = self.get_sp_name(resp_args)
        self.sp_metadata_name = sp_metadata_name
        sps_allowed = SPSService(db).get_sps_app_for_sp_redirections(user_email)
        targeted_sp_app=get_item(sps_allowed,key="sp_app_name",target=sp_metadata_name)
        if sps_allowed:
            if get_item(sps_allowed,key="sp_app_name",target=sp_metadata_name):
                return {'status_code':status.HTTP_200_OK,"targeted_sp_app_id":targeted_sp_app['id']}
            else:
                return status.HTTP_307_TEMPORARY_REDIRECT
        return status.HTTP_404_NOT_FOUND 

    def return_sp_app_name(self):
        return self.sp_metadata_name
        
    def get(self, request_parms, email,db: Session):
        from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED, NameID, NAMEID_FORMAT_TRANSIENT
        saml_msg =request_parms
        data = self.idp_server.parse_authn_request(saml_msg,BINDING_HTTP_REDIRECT)
        verify_request_signature(data)
        resp_args = self.idp_server.response_args(data.message)
        sp_metadata_name = self.get_sp_name(resp_args)
        self.sp_metadata_name = sp_metadata_name

        ## return the sp apps data
        sp_apps_data = self.query_sp_apps_sp_metadata_name(sp_metadata_name,db)
        practice_roles_data,practice_roles_status = UserService(db).get_all_sps_practice_roles_db(email)
        sps_app_object = SPSService(db)
        selected_apps = sps_app_object.get_selected_sps_app_for_idp_user(email)
        users_info, user_info_data_id = self.get_user_info(email,db)
        app_role=RolesService(db).get_user_selected_role_db_appid_userid(sp_apps_data.id,user_info_data_id )
 
        if (sp_metadata_name=='driq'):
            practice_list,roles_data,gender_data=UserService(db).get_dr_iq_user_practices_role(email)
            users_info['gender'] = gender_data
            users_info['selected_practice']=practice_list
            users_info['selected_practice'] = json.dumps(users_info['selected_practice'])
            users_info['roles']=roles_data
            users_info['roles'] = json.dumps(users_info['roles'])
            users_info['products']=selected_apps
            
        else:
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
                if app_practices_list[i]['practices']:
                    for index in range(len(app_practices_list[i]['practices'])):
                        temp_list.append(app_practices_list[i]['parent'])
                        temp_list.append(app_practices_list[i]['practices'][index]['name'])
                        try:
                            temp_list.append(app_role[1].label)
                        except Exception as e:
                            temp_list.append(None)
                        app_practices.append(str(temp_list))
                        temp_list = list([])
                else:
                    temp_list.append(app_practices_list[i]['parent'])
                    temp_list.append(None)  # Append None for 'name'
                    try:
                        temp_list.append(app_role[1].label)
                    except Exception as e:
                        temp_list.append(None)
                    app_practices.append(str(temp_list))
                    temp_list = list([])
            
            users_info['app_practices']=app_practices
            users_info['products']= selected_apps
        new_json_data = json.dumps(users_info)
        json_updated_data = json.loads(new_json_data.replace(r"\'", '"'))
        users_info["email"] = email
        identity = json_updated_data
        print('identity',identity)
        nid = NameID(name_qualifier="foo", format=NAMEID_FORMAT_TRANSIENT,
             text=email)
        value = self.idp_server.create_authn_response(identity,name_id=nid,userid=email,encrypt_cert_assertion=None,**resp_args)

        http_args = self.idp_server.apply_binding(
            binding=BINDING_HTTP_POST,
            msg_str=value,
            destination=resp_args['destination'],
            response=True)

        html_response = {
            "data": http_args,
            "type": "REDIRECT",
        }
        return html_response, resp_args
    
    
    def get_multiple_account_access(self, request_parms, sp_apps_email,primary_email,db: Session):
        from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED, NameID, NAMEID_FORMAT_TRANSIENT

        saml_msg =request_parms
        data = self.idp_server.parse_authn_request(saml_msg,BINDING_HTTP_REDIRECT)
        verify_request_signature(data)
        resp_args = self.idp_server.response_args(data.message)
        # identity =  {'username': 'Saimon4Test', 'email': 'saimon4@mailinator.com', 'first_name': 'Saimon4', 'last_name': 'Test', 'app_practices': ["['At Medics', 'Bank House Surgery', 'Accounts Manager']", "['At Medics', 'Barlby Surgery', 'Accounts Manager']", "['At Medics', 'Brunswick Medical Centre', 'Accounts Manager']", "['At Medics', 'Burnley Practice', 'Accounts Manager']", "['At Medics', 'Camden Health Improvement Practice', 'Accounts Manager']", "['At Medics', 'Canberra Old Oak Surgery', 'Accounts Manager']", "['At Medics', 'Carpenters Road Practice', 'Accounts Manager']", "['At Medics', 'Cassidy Medical Centre', 'Accounts Manager']", "['At Medics', 'E16 Health - Albert Road And Pontoon Dock', 'Accounts Manager']", "['At Medics', 'Earls Court Health And Wellbeing Centre', 'Accounts Manager']", "['At Medics', 'East One Health', 'Accounts Manager']", "['At Medics', 'Edith Cavell Surgery', 'Accounts Manager']", "['At Medics', 'Falmouth Road Group Practice', 'Accounts Manager']", "['At Medics', 'Fieldway Medical Centre', 'Accounts Manager']", "['At Medics', 'Hanley Primary Care Centre', 'Accounts Manager']", "['At Medics', 'Headley Drive Surgery', 'Accounts Manager']", "['At Medics', 'Kings Cross Surgery', 'Accounts Manager']", "['At Medics', 'Kings Road Medical Centre', 'Accounts Manager']", "['At Medics', 'Lucas Avenue Practice', 'Accounts Manager']", "['At Medics', 'Mitchison Road Surgery', 'Accounts Manager']", "['At Medics', 'Mollison Way Surgery', 'Accounts Manager']", "['At Medics', 'New Addington Group', 'Accounts Manager']", "['At Medics', 'Queens Road Practice', 'Accounts Manager']", "['At Medics', 'Randolph Surgery', 'Accounts Manager']", "['At Medics', 'Silverlock Medical Centre', 'Accounts Manager']", "['At Medics', 'Somers Town Medical Center', 'Accounts Manager']", "['At Medics', 'St. Anns Road Surgery', 'Accounts Manager']", "['At Medics', 'Streatham High Practice', 'Accounts Manager']", "['At Medics', 'Thamesmead Health Center', 'Accounts Manager']", "['At Medics', 'The Green House Surgery', 'Accounts Manager']", "['At Medics', 'The Hambleden Clinic', 'Accounts Manager']", "['At Medics', 'The Lister Practice', 'Accounts Manager']", "['At Medics', 'The Loxford Practice', 'Accounts Manager']", "['At Medics', 'The Ordnance Unity Centre For Health', 'Accounts Manager']", "['At Medics', 'The Wembley Practice', 'Accounts Manager']", "['At Medics', 'Thornton Road Surgery', 'Accounts Manager']", "['At Medics', 'Trowbridge Surgery', 'Accounts Manager']", "['At Medics', 'Valley Park Surgery', 'Accounts Manager']", "['At Medics', 'Whitechapel Health Centre', 'Accounts Manager']"], 'products': ["{'name': 'ez-login', 'logo': 'http://dev-sso-app.attech-ltd.com/api/v1/image/EZLOGO.svg', 'url': 'http://dev-sso-frontend.attech-ltd.com/'}", "{'name': 'ez-analytics', 'logo': 'http://dev-sso-app.attech-ltd.com/api/v1/image/EZANALYTICS.svg', 'url': 'https://dev.ezanalytics.co.uk/bi'}"]}
        sps_app_object = SPSService(db)
        selected_apps = sps_app_object.get_selected_sps_app_for_idp_user(primary_email)
        identity = {
        'username': primary_email,
        'email': sp_apps_email,
        'first_name': '',
        'last_name': '',
        'app_practices': [],
        'products': selected_apps
            }
        
        
        nid = NameID(name_qualifier="foo", format=NAMEID_FORMAT_TRANSIENT,
             text=sp_apps_email)
        value = self.idp_server.create_authn_response(identity,name_id=nid,userid=sp_apps_email,encrypt_cert_assertion=None,**resp_args)

        http_args = self.idp_server.apply_binding(
            binding=BINDING_HTTP_POST,
            msg_str=value,
            destination=resp_args['destination'],
            response=True)

        html_response = {
            "data": http_args,
            "type": "REDIRECT",
        }
        return html_response, resp_args