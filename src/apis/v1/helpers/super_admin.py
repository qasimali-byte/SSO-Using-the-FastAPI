from src.apis.v1.services.sps_service import SPSService
from src.apis.v1.models.idp_users_model import idp_users
from src.apis.v1.services.auth_service import AuthService
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime

from src.apis.v1.utils.auth_utils import create_password_hash
from src.apis.v1.models.user_idp_sp_apps_model import user_idp_sp_app
def create_super_admin(db: Session):
    

    # Current date time in local system
    # print(datetime.now())
    try:
        hashed_password = create_password_hash("admin")
        check = idp_users(
            uuid = uuid4(),
            organization_id = "2",
            username = "umair",
            title = None,
            first_name = "mohammad",
            last_name = "umair",
            email = "umair@gmail.com",
            other_email = "syedfaisal2@gmail.com",
            gender = "male",
            nhs_number = "4",
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
        db.add(check)
        db.commit()
        data = SPSService(db).get_sps_app_by_name("ez-nav")
        # check.sp_apps_relation.is_accessible = True
        # check.sp_apps_relation.sp_apps_id = data.id
        statement = user_idp_sp_app.insert().values(idp_users_id=check.id,  sp_apps_id=data.id, is_accessible=True)
        db.execute(statement)
        db.commit()
        # check = AuthService(db).get_idp_user("umair@gmail.com")
        print(vars(check))
    except Exception as e:
        print(e)