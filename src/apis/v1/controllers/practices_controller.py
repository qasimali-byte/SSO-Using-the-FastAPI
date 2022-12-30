from src.apis.v1.services.practices_service import PracticesService
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.validators.practices_validator import ListPracticesGeneralValidator


class PracticesController:
    def __init__(self, db):
        self.db = db

    def assign_practices_to_user(self, **kwargs):
        return PracticesService(self.db).assign_practices_user_db(**kwargs)

    def get_allowed_practices_by_userid(self, app_id, user_id, selected_id):

        practices_object = PracticesService(self.db)
        total_practices_allowed = practices_object.get_selected_practices_db_by_id(app_id,user_id, selected_id)
        return total_practices_allowed
    
    def get_allowed_practices_by_userid_loged_in_user(self, app_id, user_id, selected_id):

        practices_object = PracticesService(self.db)
        total_practices_allowed = practices_object.get_selected_practices_db_by_id_loged_in_user(app_id,user_id, selected_id)
        return total_practices_allowed

    def get_practices_by_product(self, app_name:str):
        practices_object = PracticesService(self.db).get_practices_db_by_app_name(app_name)
        # print(practices_object)
        return ListPracticesGeneralValidator.from_orm(practices_object).dict()

    def create_practice(self, practice_data):
        # ## create user in db
        practices_object = PracticesService(self.db)
        message, status_code = practices_object.create_practice_db(practice_data)
        response = custom_response(data=message, status_code=status_code)
        return response

    def delete_practice(self, practice_id):
        # Delete practice
        practices_object = PracticesService(self.db)
        message, status_code = practices_object.delete_practice_db(practice_id)
        response = custom_response(data=message, status_code=status_code)
        return response
