from src.apis.v1.services.auth_service import AuthService
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime

from src.apis.v1.utils.auth_utils import create_password_hash
def create_super_admin(db: Session):
    

    # Current date time in local system
    # print(datetime.now())
    try:
        hashed_password = create_password_hash("admin")
        check = AuthService(db).insert_idp_user(
            uuid = uuid4(),
            organization_id = "1",
            username = "syed faisal",
            title = None,
            first_name = "syed",
            last_name = "faisal",
            email = "syed@gmail.com",
            other_email = "syedfaisal2@gmail.com",
            gender = "male",
            nhs_number = "1234",
            password_hash = hashed_password,
            reset_password_token = "nothing",
            reset_password_token_expiry = "nothing",
            profile_image = None,
            contact_no = "2222222222",
            address = "nothing",
            is_approved = True,
            is_rejected = False,
            is_on_hold = False,
            is_superuser = True,
            is_active = True,
            created_date = datetime.now(),
            updated_date = datetime.now(),
            last_login_date = datetime.now()
            )

        print(check)
    except Exception as e:
        print(e)