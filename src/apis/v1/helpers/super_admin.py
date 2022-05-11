from src.apis.v1.controllers.auth_controller import AuthController
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime
def create_super_admin(db: Session):
    

    # Current date time in local system
    # print(datetime.now())
    try:
        check = AuthController(db).insert(
            uuid = uuid4(),
            organization_id = "1",
            username = "syed faisal",
            title = None,
            first_name = "syed",
            last_name = "faisal",
            email = "syedfaisal@gmail.com",
            other_email = "syedfaisal2@gmail.com",
            gender = "male",
            nhs_number = "1234",
            password_hash = "admin",
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