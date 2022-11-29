# from tests.production.api_v1.global_test_variables import TestVariables
# from test_production import client
from src.apis.v1.validators.auth_validators import EmailValidatorOut

def test_01_email_verification():
    pass
    # response = client.post("/api/v1/email-verifier", json={"email": "umair@gmail.com"})
    # assert response.status_code == 200
    # assert EmailValidatorOut(**response.json())