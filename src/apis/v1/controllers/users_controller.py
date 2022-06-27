from datetime import datetime
from lib2to3.pytree import type_repr
import typing
from src.apis.v1.helpers.customize_response import custom_response
from fastapi import status
from src.apis.v1.validators.common_validators import ErrorResponseValidator
from src.apis.v1.services.users_service import UsersService
from src.apis.v1.validators.users_validator import UsersValidator, UsersValidatorOut
class UsersController():
    def __init__(self, db) -> None:
        self.db = db
        
    def get_users(self):
        try:
            users_info, uses_info_status = UsersService(self.db).get_users_info_db()
            data = UsersValidatorOut(users_data=users_info,message="Users data retrieved Sucessfully",status_code=uses_info_status)
            response = custom_response(data=data,status_code=status.HTTP_200_OK)
            return response
        except Exception as e:
            data = ErrorResponseValidator(message="Some thing went wrong",status=False)
            response = custom_response(data=data,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response
        
