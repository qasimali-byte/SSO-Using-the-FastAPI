from src.apis.v1.controllers.roles_controller import RolesController
from src.apis.v1.controllers.practices_controller import PracticesController
from src.apis.v1.controllers.type_user_controller import TypeUserController
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.controllers.auth_controller import AuthController
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.helpers.global_helpers import create_unique_id
from src.apis.v1.services.user_service import UserService
from fastapi import status
from src.apis.v1.validators.common_validators import ErrorResponseValidator
from src.apis.v1.validators.user_validator import  CreateUserValidator, UserInfoValidator, UserSPPracticeRoleValidatorOut, UserValidatorOut
from ..utils.user_utils import format_data_for_create_user
class UsersController():
    def __init__(self, db) -> None:
        self.db = db

    def create_user(self, user_data):
        """
            Create User Controller
        """
        # ## verify valid ids of sp applications , roles, sub roles and practices
        # ## roles must be atleast selected when the app is selected roles cannot be empty
        
        # ## format data for create user
        apps_ids_list, practices_ids_list, selected_roles_list = format_data_for_create_user(user_data)

        ## verify if user already exists
        check_email = AuthController(self.db).email_verification(user_data['email'])
        if check_email.status_code == 200:
            data = ErrorResponseValidator(message="User Already Exsists")
            response = custom_response(status_code=status.HTTP_409_CONFLICT, data=data)
            return response

        # ## get type of user
        user_type_id = TypeUserController(self.db).get_type_of_user(user_data['type_of_user'])['id']

        # ## create user data
        idp_user_data = CreateUserValidator(uuid=create_unique_id(),firstname=user_data['firstname'], lastname=user_data['lastname'], email=user_data['email'],
         username=str(user_data['firstname'])+str(user_data['lastname']),user_type_id=user_type_id )
        
        # ## create user in db
        user_created_data = UserService(self.db).create_internal_user_db(idp_user_data.dict())
        user_id = user_created_data.id

        # assign sp apps to user
        SPSController(self.db).assign_sps_to_user(user_id=user_id, sps_object_list=apps_ids_list)

        # ## assign sp practices to user
        PracticesController(self.db).assign_practices_to_user(user_id=user_id, practices_list=practices_ids_list)

        # ## assign sp roles to user
        RolesController(self.db).assign_roles_to_user(user_id=user_id, roles_list=selected_roles_list)

        data = UserValidatorOut()
        response = custom_response(status_code=status.HTTP_201_CREATED, data=data)
        return response



    def get_sps_practice_roles(self, user_email):

        # user_email = "faisal@example.com"
        practice_roles_data, practice_roles_status = UserService(self.db).get_all_sps_practice_roles_db(user_email)
        if practice_roles_status != 200:
            data = ErrorResponseValidator(message=practice_roles_data)
            response = custom_response(status_code=practice_roles_status, data=data)
            return response

        try:
            data = UserSPPracticeRoleValidatorOut(sp_practice_roles=practice_roles_data)
        except Exception as e:
            data = ErrorResponseValidator(message=str(e))
            response = custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=data)
            return response
        response = custom_response(status_code=practice_roles_status, data=data)
        return response

    def get_user_info(self, user_email):
        """
            Get User Information Controller
        """
        user_info_data = UserService(self.db).get_user_info_db(user_email)
        user_info_resp = UserInfoValidator(user_info = user_info_data,statuscode=status.HTTP_200_OK, message="User Info Found")
        response = custom_response(status_code=status.HTTP_200_OK, data=user_info_resp)
        return response


    def update_user_info(self, user_email, user_data):
        """
            Update User Information Controller
        """
        user_data['email'] = user_email
        
        ## update user info in db
        UserService(self.db).update_user_info_db(user_data)

        user_info_resp = UserInfoValidator(user_info= user_data, statuscode=status.HTTP_201_CREATED, message="User Info Updated")
        response = custom_response(status_code=status.HTTP_201_CREATED, data=user_info_resp)
        return response
        