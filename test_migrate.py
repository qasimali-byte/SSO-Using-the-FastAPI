from contextlib import contextmanager
import requests
import load_env
from src.apis.v1.controllers.async_sps_controller import AsyncSpsController
from src.apis.v1.controllers.practices_controller import PracticesController
from src.apis.v1.controllers.roles_controller import RolesController
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.db.session import get_db
from src.apis.v1.services.practices_service import PracticesService
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
# from src.packages.saml2_local.idp_local_server import Saml2LocalServer


class UserMigrate:
    def __init__(self) -> None:
        self.idp_server = idp_local_server.Saml2LocalServer(config_file="idp/idp_conf.py")
        self.db = None

    def product_details(self, app_id) -> tuple:
        get_product = SPSController(self.db).get_specific_product_byappid(app_id)
        return (get_product['__root__'][0]['sp_metadata'],get_product['__root__'][0]['migration_url'])

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
        print(practice_ids)
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
                    practices_ids.append(practice['id'])
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

# UserMigrate().user_migration_request()
