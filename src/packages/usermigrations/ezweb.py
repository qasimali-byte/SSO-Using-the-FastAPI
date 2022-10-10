from contextlib import contextmanager
from fastapi import status
import requests
from src.apis.v1.controllers.practices_controller import PracticesController
from src.apis.v1.controllers.roles_controller import RolesController
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.db.session import get_db
from src.apis.v1.helpers.custom_exceptions import CustomException


class EZWEBMigrate:
    
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
        except Exception:
            raise CustomException(message="ez web not working", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


