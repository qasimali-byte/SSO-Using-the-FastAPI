from contextlib import contextmanager
from fastapi import HTTPException
import requests
import load_env
from src.apis.v1.controllers.async_sps_controller import AsyncSpsController
from src.apis.v1.controllers.practices_controller import PracticesController
from src.apis.v1.controllers.roles_controller import RolesController
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.db.session import get_db
from src.apis.v1.services.practices_service import PracticesService
from src.apis.v1.services.sps_service import SPSService
from src.apis.v1.services.user_service import UserService
from src.apis.v1.validators.sps_validator import SpAppsGeneralValidator
from src.graphql.db.session import get_session
from src.packages.saml2_local import idp_local_server
from saml2 import config
from saml2.client import Saml2Client
from saml2.saml import NAMEID_FORMAT_PERSISTENT, EncryptedAssertion, Advice
from saml2.saml import NAMEID_FORMAT_TRANSIENT
from saml2.saml import NameID
from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    entity,
    BINDING_SOAP
)
from saml2.time_util import in_a_while
from sqlalchemy.orm import Session
import json
# from src.packages.saml2_local.idp_local_server import Saml2LocalServer


class UserMigrate:
    def __init__(self) -> None:
        self.idp_server = idp_local_server.Saml2LocalServer(config_file="idp/idp_conf.py")
        self.db = None

    def product_details(self, app_id) -> tuple:
        get_product = SPSController(self.db).get_specific_product_byappid(app_id)
        return (get_product['__root__'][0]['sp_metadata'],get_product['__root__'][0]['migration_url'])

    def get_user_info(self, email,db: Session):
        user_info_data = UserService(db).get_user_info_db(email)
        users_info = dict({
            "username": user_info_data.username,
            "email": user_info_data.email,
            "first_name": user_info_data.first_name,
            "last_name": user_info_data.last_name


        })
        return users_info, user_info_data.id
            
    def query_sp_apps_sp_metadata_name(self, sp_name, db: Session):
        sps_object = SPSService(db).get_sps_app_by_filter(sp_metadata=sp_name)
        if sps_object:
            return SpAppsGeneralValidator.from_orm(sps_object[0])
        else:
            raise HTTPException(status_code=500, detail="NO SP APP FOUND")
            
    def get(self, email,db: Session):
        from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED, NameID, NAMEID_FORMAT_TRANSIENT
        from src.apis.v1.services import sps_service, roles_service, user_service

        self.sp_metadata_name = 'ezanalytics'

        ## return the sp apps data
        sp_apps_data = self.query_sp_apps_sp_metadata_name(self.sp_metadata_name,db)
        practice_roles_data,practice_roles_status = user_service.UserService(db).get_all_sps_practice_roles_db(email)
        sps_app_object = sps_service.SPSService(db)
        selected_apps = sps_app_object.get_selected_sps_app_for_idp_user(email)
        users_info, user_info_data_id = self.get_user_info(email,db)
        app_role = roles_service.RolesService(db).get_user_selected_role_db_appid_userid(sp_apps_data.id,user_info_data_id )
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
        users_info['products']= selected_apps
        new_json_data = json.dumps(users_info)
        json_updated_data = json.loads(new_json_data.replace(r"\'", '"'))
        users_info["email"] = email
        identity = json_updated_data


        nid = NameID(name_qualifier="foo", format=NAMEID_FORMAT_TRANSIENT,
             text=email)
        value = self.idp_server.create_authn_response(identity,name_id=nid,userid=email,encrypt_cert_assertion=None,destination='http://localhost:3000')

        http_args = self.idp_server.apply_binding(
            binding=BINDING_HTTP_POST,
            msg_str=value,
            # destination=resp_args['destination'],
            response=True)

        html_response = {
            "data": http_args,
            "type": "REDIRECT",
        }
        print(html_response)
        # return html_response, resp_args

    def user_migration_request(self, email, app_id):
        with contextmanager(get_db)() as session:  # execute until yield. Session is yielded value
            self.db = session

        # nid = NameID(name_qualifier="foo", format=NAMEID_FORMAT_TRANSIENT,
        #      text="123456")

        # t_l = [
        #     "loadbalancer-91.siroe.com",
        # ]
        # t_l_2 = {
        #     "loadbalancer-91.siroe.com": "http://localhost:8088/api/v1/test1"
        # }


        # req_id, req = self.idp_server.create_migrate_request(
        #     issuer_entity_id=t_l[0],
        #     destination=t_l_2[t_l[0]],
        #     name_id=nid, reason="Tired", expire=in_a_while(minutes=15),
        #     session_indexes=["_foo"])

        # info = self.idp_server.apply_binding(
        #     BINDING_SOAP, req, t_l_2[t_l[0]],
        #     relay_state="relay2")
        # redirect_url = None
        # print(info)
        # response = ""

        app_data = self.product_details(app_id)
        practices_app = self.practices_data_by_app_name(app_data[0])
        try:
            response = requests.post(app_data[1], json={'email':email,'type':'migration'})
        except Exception as e:
            print(e, "----e")

        response = response.json()
        practice_ids = self.validate_practices_data_by_response(response['data']['selected_practice'],practices_app['__root__'])
        roles_data = self.roles_data_by_app_id(app_id)
        role_id = self.validate_roles_by_response_role(response['data']['role'],roles_data)
        return {
            'id':app_id,
            'practices':practice_ids,
            'role':{
                'id':role_id,
                'sub_role': None
            }
        }

    def practices_data_by_app_name(self, app_name):
        return PracticesController(self.db).get_practices_by_product(app_name)

    def roles_data_by_app_id(self, app_id):
        return RolesController(self.db).get_roles_by_app_id(app_id=app_id)

    def validate_practices_data_by_response(self, response_data, practice_data):
        practices_ids = []
        for values in response_data:
            for practice in practice_data:
                if values.lower() == practice['name'].lower():
                    practices_ids.append({'id':practice['id']})
        return practices_ids

    def validate_roles_by_response_role(self, response_roles_data, roles_data):
        for role in roles_data:
            if role['name'].lower() == response_roles_data.lower():
                return role['id']

        if len(roles_data) > 0:
            return roles_data[0]['id']

        else:
            return None

    def storing_migration_data():
        pass

with contextmanager(get_db)() as session:  # execute until yield. Session is yielded value
    db = session
UserMigrate().get('umair@gmail.com', db)
