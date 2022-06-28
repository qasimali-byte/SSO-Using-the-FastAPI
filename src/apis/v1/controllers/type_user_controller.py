from src.apis.v1.services.type_of_user_service import TypeOfUserService
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.validators.common_validators import ErrorResponseValidator
from fastapi import status



class TypeUserController():
    def __init__(self, db):
        self.db = db
    
    def get_type_of_user(self,type_of_user):
        return TypeOfUserService(self.db).get_type_of_user_db(type_of_user)
        
    def get_type_of_user_service(self,type_of_user):
        try:
            data = self.get_type_of_user(type_of_user)
            response = custom_response(status_code=status.HTTP_200_OK, data=data)
            return response
        except Exception as e:
            data = ErrorResponseValidator(message=str(e))
            response = custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=data)
            return response