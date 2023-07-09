from contextlib import contextmanager
from fastapi import status
import requests
from src.apis.v1.controllers.practices_controller import PracticesController
from src.apis.v1.controllers.roles_controller import RolesController
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.db.session import get_db
from src.apis.v1.helpers.custom_exceptions import CustomException


class EZAnalyticsMigrate:
    
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
        try:
            response = requests.post(app_data[1], json={'email':email,'type':'migration'})
        except Exception as e:
            print(e)
            raise CustomException(message="ez analytics not working", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response = response.json()
        first_name = response['Data']['first_name']
        last_name = response['Data']['last_name']
        contact_no=response['Data']['contact_no']
        roles_data = self.roles_data_by_app_id(app_id)
        if len(response['Data']['selected_practice']) < 1:
            return {
            'first_name':first_name,
            'last_name':last_name,
            'contact_no':contact_no,
            'dr_iq_gender_id':None,
            'id':app_id,
            'practices': [],
            'role':{
                'id':roles_data[0]['id'],
                'sub_role': None
                }
            }

            # raise CustomException(message="ez analytics user contains no practice", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        practice_ids = self.validate_practices_data_by_response(response['Data']['selected_practice'],practices_app['__root__'])
        
        role_id = self.validate_roles_by_response_role(response['Data']['selected_practice'][0]['role'],roles_data)
        return {
            'first_name':first_name,
            'last_name':last_name,
            'contact_no':contact_no,
            'dr_iq_gender_id':None,
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
        empty_practice_set = set()
        for values in response_data:
            for practice in practice_data:
                if values['practice'].lower() == practice['name'].lower():
                    if practice['id'] not in empty_practice_set:
                        practices_ids.append({'id':practice['id']})
                        empty_practice_set.add(practice['id'])
                
                if values['parent_organization'].lower() if values['parent_organization'] else None == practice['name'].lower():
                    if practice['id'] not in empty_practice_set:
                        practices_ids.append({'id':practice['id']})
                        empty_practice_set.add(practice['id'])

        return practices_ids

    def validate_roles_by_response_role(self, response_roles_data, roles_data):
        for role in roles_data:
            if role['name'].lower() == response_roles_data.lower():
                return role['id']

        if len(roles_data) > 0:
            return roles_data[0]['id']

        else:
            return None
