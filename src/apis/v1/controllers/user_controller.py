from datetime import datetime
from src.apis.v1.services.type_of_user_service import TypeOfUserService
from src.apis.v1.utils.user_utils import image_writer
from src.apis.v1.controllers.roles_controller import RolesController
from src.apis.v1.controllers.practices_controller import PracticesController
from src.apis.v1.controllers.type_user_controller import TypeUserController
from src.apis.v1.helpers.custom_exceptions import CustomException
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.controllers.auth_controller import AuthController
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.helpers.global_helpers import create_unique_id
from src.apis.v1.services.user_service import UserService
from fastapi import status
from src.apis.v1.validators.users_validator import UsersValidatorOut
from src.apis.v1.validators.common_validators import ErrorResponseValidator, SuccessfulJsonResponseValidator
from src.apis.v1.validators.user_validator import  CreateUserValidator, GetUsersValidatorUpdateApps, \
    UpdateUserValidatorDataClass, UserInfoValidator, UserSPPracticeRoleValidatorOut, UserValidatorOut,UserDeleteValidatorOut
from ..utils.user_utils import check_driq_gender_id_exsist, format_data_for_create_user, format_data_for_update_user_image

class UserController():
    def __init__(self, db) -> None:
        self.db = db

    def assign_practices_apps_roles(self, user_id:int, apps_ids_list, practices_ids_list, selected_roles_list) -> int:

        # assign sp apps to user
        SPSController(self.db).assign_sps_to_user(user_id=user_id, sps_object_list=apps_ids_list)

        # ## assign sp practices to user
        PracticesController(self.db).assign_practices_to_user(user_id=user_id, practices_list=practices_ids_list)

        # ## assign sp roles to user
        RolesController(self.db).assign_roles_to_user(user_id=user_id, roles_list=selected_roles_list)

        return 200

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

        ## check and assign dr iq gender id to user
        driq_gender_id = check_driq_gender_id_exsist(user_data)

        # ## create user data
        idp_user_data = CreateUserValidator(uuid=create_unique_id(),firstname=user_data['firstname'], lastname=user_data['lastname'], email=user_data['email'],
         username=str(user_data['firstname'])+str(user_data['lastname']),user_type_id=user_type_id,dr_iq_gender_id=driq_gender_id)
        
        # ## create user in db
        user_created_data = UserService(self.db).create_user_db(idp_user_data.dict())
        user_id = user_created_data.id

        self.assign_practices_apps_roles(user_id=user_id, apps_ids_list=apps_ids_list, practices_ids_list=practices_ids_list, selected_roles_list=selected_roles_list)

        data = UserValidatorOut()
        response = custom_response(status_code=status.HTTP_201_CREATED, data=data)
        return response

    def get_sps_practice_roles(self, user_email):

        practice_roles_data, practice_roles_status = UserService(self.db).get_all_sps_practice_roles_db(user_email)
        if practice_roles_status != 200:
            data = ErrorResponseValidator(message=practice_roles_data)
            response = custom_response(status_code=practice_roles_status, data=data)
            return response

        try:
            data = UserSPPracticeRoleValidatorOut(sp_practice_roles=practice_roles_data)
            data = data.dict(exclude_none=True)
        except Exception as e:
            data = ErrorResponseValidator(message=str(e))
            response = custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=data)
            return response
        response = custom_response(status_code=practice_roles_status, data=data)
        return response



    def get_user_practices_roles_by_id(self, user_email:str, user_id:int):
        """
            Get User Practices And Selected Roles By ID
         """
        selected_user_id = user_id
        user_service_object = UserService(self.db) 
        user_info = user_service_object.get_user_info_db(user_email)  
        selected_user_info = user_service_object.get_user_info_db_by_id(user_id)
        if selected_user_info is None:
            data = ErrorResponseValidator(message="User Not Found")
            response = custom_response(status_code=status.HTTP_404_NOT_FOUND, data=data)
            return response
        
        selected_email = selected_user_info.email
        allowed_apps = SPSController(self.db).get_allowed_apps_by_userid(user_email, selected_email, user_info.id, selected_user_id)
        firstname = selected_user_info.first_name
        lastname = selected_user_info.last_name
        type_of_user = TypeOfUserService(self.db).get_type_of_user_db_by_userid(selected_user_id)
        type_of_user = type_of_user['name']
        data = GetUsersValidatorUpdateApps(firstname=firstname, lastname=lastname, 
        email=selected_email, type_of_user=type_of_user, sp_practice_roles=allowed_apps, is_active=selected_user_info.is_active)
        response = custom_response(status_code=status.HTTP_200_OK, data=data)
        return response

    def update_user_practices_roles_by_id(self, user_id:int, user_data):
        """
            Update User Practices, SP Applications And Roles By User ID
        """
        # ## format data for create user
        apps_ids_list, practices_ids_list, selected_roles_list = format_data_for_create_user(user_data)

        # ## get type of user
        user_type_id = TypeUserController(self.db).get_type_of_user(user_data['type_of_user'])['id']

        user_service_object = UserService(self.db) 
        selected_user_info = user_service_object.get_user_info_db_by_id(user_id)
        if selected_user_info is None:
            data = ErrorResponseValidator(message="User Not Found")
            response = custom_response(status_code=status.HTTP_404_NOT_FOUND, data=data)
            return response
        
        ## delete user sp apps, practices and roles
        user_service_object.delete_user_practices_roles_db(user_id)
        
        ## check and assign dr iq gender id to user
        driq_gender_id = check_driq_gender_id_exsist(user_data)

        idp_user_data = UpdateUserValidatorDataClass(firstname=user_data['firstname'], lastname=user_data['lastname'],
        updated_date=datetime.now(),username=user_data['firstname']+user_data['lastname'], is_active=user_data['is_active'],
        dr_iq_gender_id=driq_gender_id,user_type_id=user_type_id)

        idp_user_data = idp_user_data.dict()
        idp_user_data['id'] = user_id

        ## update user id column in idp users
        user_service_object.update_user_info_db_by_id(idp_user_data)

        ## assign sp applications, practices and roles to user
        self.assign_practices_apps_roles(user_id=user_id, apps_ids_list=apps_ids_list, practices_ids_list=practices_ids_list, selected_roles_list=selected_roles_list)
        
        data = {
            "message": "successfully updated user practices, apps and roles",
            "statuscode": status.HTTP_201_CREATED
        }
        validated_data = SuccessfulJsonResponseValidator(**data)
        response = custom_response(status_code=status.HTTP_201_CREATED, data=validated_data)
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
    
    def delete_user(self,user_id):
        """
            this function will delete the user
        """

        message,status_code=UserService(self.db).delete_users_info_db(user_id)
        data = UserDeleteValidatorOut(message=message,status_code=status_code)
        response = custom_response(data=data,status_code=status_code)
        return response
  

    def update_user_image(self,user_email,data_image):
        """
            Update User Image Controller
        """
        data_image = format_data_for_update_user_image(data_image)
        image_url = image_writer(data_image)
        update_image_data = UserService(self.db).update_user_image_db(user_email=user_email, user_image_url=image_url)
        data = {
            "message": update_image_data,
            "statuscode": status.HTTP_201_CREATED
        }
        validated_data = SuccessfulJsonResponseValidator(**data)
        response = custom_response(status_code=status.HTTP_201_CREATED, data=validated_data)
        return response

    def get_user_by_email(self, user_email):
        """
            Get User By Email Controller
        """
        user_info_data = UserService(self.db).get_user_info_db(user_email)
        return user_info_data
        
