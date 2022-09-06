from src.apis.v1.controllers.roles_controller import RolesController
from src.apis.v1.controllers.type_user_controller import TypeUserController
from src.apis.v1.helpers.customize_response import custom_response
from fastapi import status
from src.apis.v1.services.roles_service import RolesService
from src.apis.v1.services.user_service import UserService
from src.apis.v1.services.users_service import UsersService
from src.apis.v1.validators.users_validator import UsersValidatorOut
import math

class UsersController():
    def __init__(self, db) -> None:
        self.db = db
        self._metadata = {}
        

    def get_users(self, user_email:str, page_limit:int, page_offset:int,order_by:str, latest:bool,search:str,user_status:bool,select_practices:str) -> dict:
        """
            Get Users according to the roles of user email
        """
        page_offset -= 1
        user_id = UserService(self.db).get_user_info_db(user_email)
        user_id = user_id.id
        user_selected_role = RolesService(self.db).get_user_selected_role("ez-login", user_id)

        if user_selected_role == "super-admin":
            # get subadmins and practice admins and external users
            users_info, records_count = UsersService(self.db).get_internal_external_users_info_db(user_role='super-admin',page_limit=page_limit,\
                 page_offset=page_offset,order_by=order_by, latest=latest,search=search,user_status=user_status,select_practices=select_practices)

        elif user_selected_role == "sub-admin":
            # get practice admins and external users
            users_info, records_count = UsersService(self.db).get_internal_external_users_info_db(user_role='sub-admin',page_limit=page_limit,\
                 page_offset=page_offset,order_by=order_by, latest=latest,search=search,user_status=user_status,select_practices=select_practices)

        elif user_selected_role == "practice-administrator":
            # get user type id of external user
            user_type_id = TypeUserController(self.db).get_type_of_user('external')['id']

            # get all external users from db for practice admin role
            users_info, records_count = UsersService(self.db).get_external_users_info_db(user_type_id=user_type_id,page_limit=page_limit,\
                 page_offset=page_offset,order_by=order_by, latest=latest,search=search,user_status=user_status,select_practices=select_practices)

        else:
            users_info = []
            records_count = 0

        ## structuring pagination data
        _metadata = {
            "page": page_offset+1,
            "per_page": page_limit,
            "page_count": math.ceil(records_count / page_limit),
            "total_records": records_count,
        }
        
        self._metadata = _metadata
        data = UsersValidatorOut(_metadata=self._metadata,users_data=users_info,message="Users data retrieved Sucessfully",status_code=status.HTTP_200_OK)
        response = custom_response(data=data,status_code=status.HTTP_200_OK)
        return response