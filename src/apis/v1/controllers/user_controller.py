from datetime import datetime
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.controllers.auth_controller import AuthController
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.helpers.global_helpers import create_unique_id
from src.apis.v1.services.user_service import UserService
from fastapi import status
from src.apis.v1.validators.common_validators import ErrorResponseValidator
from src.apis.v1.validators.user_validator import  UserSPPracticeRoleValidatorOut, UserValidatorOut
class UsersController():
    def __init__(self, db) -> None:
        self.db = db

    def create_internal_user(self, user_data):
        uuid = create_unique_id()
        first_name = user_data.firstname
        last_name = user_data.lastname
        username = first_name + last_name
        email = user_data.email
        nhs_number = "123456789"
        organization_id = "2"
        password_hash = str(uuid)
        reset_password_token = 'reset_password_token',
        reset_password_token_expiry = 'reset_password_token_expiry',
        created_date = datetime.now(),
        updated_date = datetime.now(),
        last_login_date = datetime.now()
        type_of_user = "internal"
        sps = user_data.apps_allowed
        internal_user_role = user_data.internal_user_role
        is_active = user_data.is_active
        

        ## verify if user already exists
        check_email = AuthController(self.db).email_verification(email)
        if check_email.status_code == 200:
            data = ErrorResponseValidator(message="User Already Exsists")
            response = custom_response(status_code=status.HTTP_409_CONFLICT, data=data)
            return response

        sps_object_list = SPSController(self.db).get_all_filtered_sps_object(sps=sps)
        sps_object_list_data = sps_object_list[0]
        sps_object_list_status = sps_object_list[1]
        if sps_object_list_status != 200:
            data = ErrorResponseValidator(message="No SPS Found")
            response = custom_response(status_code=status.HTTP_404_NOT_FOUND, data=data)
            return response

        ## creating new user
        user_created = UserService(self.db).create_internal_idp_user(uuid=uuid, first_name=first_name, last_name=last_name, username=username,
            email=email, organization_id=organization_id, nhs_number=nhs_number, password_hash=password_hash,reset_password_token=reset_password_token,
            reset_password_token_expiry=reset_password_token_expiry,is_active=is_active ,created_date=created_date, updated_date=updated_date, 
            last_login_date=last_login_date, type_of_user=type_of_user,sps_object_list=sps_object_list_data, 
            internal_user_role=internal_user_role)

        user_created_data = user_created[0]
        user_created_status = user_created[1]

        if user_created_status != 201:
            data = ErrorResponseValidator(message=user_created_data)
            response = custom_response(status_code=user_created_status, data=data)
            return response

        data = UserValidatorOut()
        response = custom_response(status_code=status.HTTP_201_CREATED, data=data)
        return response



    def get_sps_practice_roles(self):
        practice_roles_data, practice_roles_status = UserService(self.db).get_all_sps_practice_roles_db()
        if practice_roles_status != 200:
            data = ErrorResponseValidator(message=practice_roles_data)
            response = custom_response(status_code=practice_roles_status, data=data)
            return response
        try:
            data = UserSPPracticeRoleValidatorOut(sp_practice_roles=practice_roles_data)
        except Exception as e:
            data = ErrorResponseValidator(message=practice_roles_data)
            response = custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=data)
            return response
        response = custom_response(status_code=practice_roles_status, data=data)
        return response