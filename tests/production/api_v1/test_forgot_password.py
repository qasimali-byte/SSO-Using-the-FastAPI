from src.apis.v1.db.session import get_db
from src.apis.v1.models import idp_users
from tests.production.api_v1.global_test_variables import TestVariables
from test_production import client
from src.apis.v1.validators.auth_validators import EmailValidatorOut
from src.apis.v1.controllers.user_controller import UserController
import  load_env
def test_verify_email():
    class user_data():
        email = "umair@gmail.com"
        id = "230"
    uc = UserController(db=get_db())
    user_key = uc.send_email_to_user(uc, user_data=user_data)
    user_key = UserController.reset_password_through_email("umair@gmail.com")
    # user_key = "http://dev-sso-app.attech-ltd.com/api/v1/verify-email/Z0FBQUFBQm\
    # ktcmw0a2d5MlhTT0hKUjVYWHdtMGNldXBuU3dQOHlKQl9KNERXMkEybjNSWGgxU291WDY5Qm5hLUp\
    # KZkNkRkcwb083d1ZjTDluamNZOXpCSXdIYjNleGNTN2JtdWRyMTZIcU15bHNwempHYldnTG11bUUy\
    # bm4tNnNQdml4V2haTVZ0d3F6elBCc2VGVWtXOGRrSGtDcHZybjdSVXZqQUpPS1lENVBHbkxFZEpDbnhRPQ=="

    # response = client.post(f"/api/v1/email-verifier/{user_key}")
    print(user_key)

    # assert response.status_code == 202 , "Accepted"
