import logging

import shortuuid as shortuuid

from src.apis.v1.utils.user_utils import image_writer, get_encrypted_text
from src.apis.v1.controllers.roles_controller import RolesController
from src.apis.v1.controllers.practices_controller import PracticesController
from src.apis.v1.controllers.type_user_controller import TypeUserController
from src.apis.v1.core.project_settings import Settings
from src.apis.v1.helpers.customize_response import custom_response
from src.apis.v1.controllers.auth_controller import AuthController
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.helpers.global_helpers import create_unique_id
from src.apis.v1.services.user_service import UserService
from src.apis.v1.workers.worker import create_task
from fastapi import status
from src.apis.v1.validators.common_validators import ErrorResponseValidator, SuccessfulJsonResponseValidator
from src.apis.v1.validators.user_validator import CreateUserValidator, UserInfoValidator, \
    UserSPPracticeRoleValidatorOut, UserValidatorOut
from ..utils.user_utils import format_data_for_create_user, format_data_for_update_user_image


class UsersController():
    def __init__(self, db) -> None:
        self.db = db
        self.log = logging.getLogger(__name__)

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
        idp_user_data = CreateUserValidator(uuid=create_unique_id(), firstname=user_data['firstname'],
                                            lastname=user_data['lastname'], email=user_data['email'],
                                            username=str(user_data['firstname']) + str(user_data['lastname']),
                                            user_type_id=user_type_id)

        # ## create user in db
        user_created_data = UserService(self.db).create_user_db(idp_user_data.dict())
        user_id = user_created_data.id

        # assign sp apps to user
        SPSController(self.db).assign_sps_to_user(user_id=user_id, sps_object_list=apps_ids_list)

        # ## assign sp practices to user
        PracticesController(self.db).assign_practices_to_user(user_id=user_id, practices_list=practices_ids_list)

        # ## assign sp roles to user
        RolesController(self.db).assign_roles_to_user(user_id=user_id, roles_list=selected_roles_list)

        data = UserValidatorOut()
        self.send_email_to_user(user_id=user_id, user_email=user_data['email'])
        response = custom_response(status_code=status.HTTP_201_CREATED, data=data)
        return response

    def send_email_to_user(self, user_id, user_email):
        encrypted_id = get_encrypted_text(user_id)
        task = create_task.delay(encrypted_user_id=encrypted_id, user_email=user_email)
        self.log.info(f"Task created: task={task.id},user_id={user_id}, encrypted_id={encrypted_id}, \
        user_email={user_email}")
        print(f"Task created: task={task.id},user_id={user_id}, encrypted_id={encrypted_id}, user_email={user_email}")


    def get_sps_practice_roles(self, user_email):

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
        user_info_resp = UserInfoValidator(user_info=user_info_data, statuscode=status.HTTP_200_OK,
                                           message="User Info Found")
        response = custom_response(status_code=status.HTTP_200_OK, data=user_info_resp)
        return response

    def update_user_info(self, user_email, user_data):
        """
            Update User Information Controller
        """
        user_data['email'] = user_email

        ## update user info in db
        UserService(self.db).update_user_info_db(user_data)

        user_info_resp = UserInfoValidator(user_info=user_data, statuscode=status.HTTP_201_CREATED,
                                           message="User Info Updated")
        response = custom_response(status_code=status.HTTP_201_CREATED, data=user_info_resp)
        return response

    def update_user_image(self, user_email, data_image):
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
