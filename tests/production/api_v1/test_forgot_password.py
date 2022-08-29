from time import sleep

import requests
from fastapi import Depends
from sqlalchemy.orm import Session

from src.apis.v1.db.session import get_db, SessionLocal
from src.apis.v1.models import idp_users
from tests.production.api_v1.global_test_variables import TestVariables
from test_production import client
from src.apis.v1.validators.auth_validators import EmailValidatorOut
from src.apis.v1.controllers.user_controller import UserController
import load_env
from tests.production.utils.email_url_scraper import read_email_from_gmail
from global_test_variables import TestVariables


def test_change_password():
    response = client.post("api/v1/change-password", json={"email": "umair@gmail.com"})
    print("Test Change Password ===>", "Passed" if response.status_code==202 else "Failed")
    assert response.status_code == 202


def test_verify_email():
    class user_data():
        first_name = "asad"
        email = TestVariables.demo_forgot_password_email
        id = "1824"

    uc = UserController(SessionLocal())
    user_key = uc.send_email_to_user(uc, user_data=user_data)
    # print("user_key : ",user_key)
    # wait for 30 seconds to ensure that email is received by the user. removing asynk await for test.
    sleep(15)
    # grab 5 latest emails from user's email account.
    email_verification_url = read_email_from_gmail(1, True)
    assert user_key == email_verification_url
    # # now verify verifi_url.
    # response = client.get(email_verification_url.split('/')[-1])

    session = requests.Session()
    response = session.get(email_verification_url)
    print("Test Verify Email ===>", "Passed" if response.status_code == 200 else "Failed")
    assert response.status_code == 200
    # print(session.cookies.get_dict())
    if session.cookies:
        TestVariables.reset_password_cookies = session.cookies.get("ssid")
        print("Session Cookies Saved : ",session.cookies.get_dict())


def test_set_password():
    # it also takes cookies with it , sent by verify_email.
    print("Test Set Password , cookie from Test Veriables : ", "e03b84f4734f4737894f80ab03467ae5")
    response = client.post("api/v1/set-password", json={"password": "My@Password13"},
                           cookies={'ssid': TestVariables.reset_password_cookies})
    print("Test Set Password ===>", "Passed" if response.status_code==202 else "Failed")
    assert response.status_code == 202
