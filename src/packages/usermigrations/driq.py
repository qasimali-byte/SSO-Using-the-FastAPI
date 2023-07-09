from contextlib import contextmanager
import json
from fastapi import status
import requests
from src.apis.v1.controllers.practices_controller import PracticesController
from src.apis.v1.controllers.roles_controller import RolesController
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.db.session import get_db
from src.apis.v1.helpers.custom_exceptions import CustomException
from src.apis.v1.services.gender_service import GenderService


class DRIQMigrate:
    
    def __init__(self) -> None:
        self.db = None

    def product_details(self, app_id) -> tuple:
        get_product = SPSController(self.db).get_specific_product_byappid(app_id)
        return (get_product['__root__'][0]['sp_metadata'],get_product['__root__'][0]['migration_url'])

    def user_migration_request(self, email, app_id):
        with contextmanager(get_db)() as session:  # execute until yield. Session is yielded value
            self.db = session

        app_data = self.product_details(app_id)
        practices_app = self.practices_data_by_app_name(app_data[0])
        gender_data = GenderService(self.db).get_genders_db()
        try:
            payload={'email':email,'type':'migration'}
            response = requests.request("POST", app_data[1],  data=payload)
        except Exception:
            raise CustomException(message="dr iq not working", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = response.json()
        # this  code will comment out

        # Add the missing keys
        # response['data']['roles']['dr_iq_role'] = {'id': '3', 'title': 'Practice Admin'}
        # response['data']['roles']['practice_role'] = {'id': '30', 'title': 'Manager'}

        roles_data = self.roles_data_by_app_id(app_id)

        dr_iq_role_id = self.validate_dr_iq_role_by_response_role(response['data']['roles']['dr_iq_role']['title'],roles_data)
        dr_iq_practice_role_id=self.validate_dr_iq_practice_role_by_response_role(response['data']['roles']['practice_role']['title'],roles_data)
        first_name = response['data']['first_name']
        last_name = response['data']['last_name']
        contact_no=response['data']['contact_no']
        dr_iq_geder_data = self.validate_gender_data_by_response(gender_data,response['data']['gender'])
        if len(response['data']['selected_practice']) < 1:
            return {
            'first_name':first_name,
            'last_name':last_name,
            'contact_no':contact_no,
            'dr_iq_gender_id':dr_iq_geder_data,
            'id':app_id,
            'practices': [],
            'role':{
                'id':dr_iq_role_id,
                'sub_role': dr_iq_practice_role_id
                }
            }
        
        
        practice_ids = self.validate_practices_data_by_response(response['data']['selected_practice'],practices_app['__root__'])
        
        return {
            'first_name':first_name,
            'last_name':last_name,
            'contact_no':contact_no,
            'dr_iq_gender_id':dr_iq_geder_data,
            'id':app_id,
            'practices':practice_ids,
            'role':{
                'id':dr_iq_role_id,
                'sub_role': dr_iq_practice_role_id
            }
        }
        
    def practices_data_by_app_name(self, app_name):
        return PracticesController(self.db).get_practices_by_product(app_name)
    
    def roles_data_by_app_id(self, app_id):
        return RolesController(self.db).get_roles_by_app_id(app_id=app_id)
    
    def validate_dr_iq_role_by_response_role(self, response_roles_data, roles_data):
        for role in roles_data:
            if role['name'].lower() == response_roles_data.lower():
                return role['id']

        if len(roles_data) > 0:
            return roles_data[0]['id']

        else:
            return None
        
    def validate_dr_iq_practice_role_by_response_role(self, response_roles_data, roles_data):
        for role in roles_data:
            for sub_role in role['sub_roles']:
                if sub_role['name'].lower() == response_roles_data.lower():
                    return sub_role['id']

        if len(roles_data) > 0 and len(roles_data[0]['sub_roles']) > 0:
            return roles_data[0]['sub_roles'][0]['id']

        else:
            return None
        
    def validate_practices_data_by_response(self, response_data, practice_data):
        practices_ids = []
        for values in response_data[0]:
            for practice in practice_data:
                if values['name'].lower() == practice['name'].lower():
                    practices_ids.append({'id':practice['id'],'region_id':practice['region_id']})             
        return practices_ids
    def validate_gender_data_by_response(self, response_gender_data, gender_data):
        for gender in response_gender_data['gender']:
            if gender['name'].lower() == gender_data.lower():
                return gender['id']
        return None