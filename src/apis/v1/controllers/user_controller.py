from datetime import datetime
from src.apis.v1.controllers.sps_controller import SPSController
from src.apis.v1.helpers.global_helpers import create_unique_id
from src.apis.v1.services.user_service import UserService

class UsersController():
    def __init__(self, db) -> None:
        self.db = db

    def create_internal_user(self, **kwargs) -> None:
        uuid = create_unique_id()
        first_name = "faisal"
        last_name = "saleem"
        username = first_name + last_name
        email = "syedfaisalsaleem@gmail.com"
        nhs_number = "123456789"
        organization_id = "2"
        password_hash = str(uuid)
        reset_password_token = 'reset_password_token',
        reset_password_token_expiry = 'reset_password_token_expiry',
        created_date = datetime.now(),
        updated_date = datetime.now(),
        last_login_date = datetime.now()
        type_of_user = "internal"

        ## verify if user already exists
        sps = [
            'dr-iq',
            'ez-doc'
        ]
        sps_object_list = SPSController(self.db).get_all_filtered_sps_object(sps=sps)[0]
        print(sps_object_list)
        

        ## creating new user
        UserService(self.db).create_internal_idp_user(uuid=uuid, first_name=first_name, last_name=last_name, username=username,
            email=email, organization_id=organization_id, nhs_number=nhs_number, password_hash=password_hash,reset_password_token=reset_password_token,
            reset_password_token_expiry=reset_password_token_expiry, created_date=created_date, updated_date=updated_date, 
            last_login_date=last_login_date, type_of_user=type_of_user,sps_object_list=sps_object_list)