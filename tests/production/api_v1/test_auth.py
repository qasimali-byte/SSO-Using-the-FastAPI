from tests.production.api_v1.global_test_variables import TestVariables
from test_production import client
from src.apis.v1.validators.auth_validators import EmailValidatorOut

def test_01_email_verification():
    response = client.post("/api/v1/email-verifier", json={"email": "umair@gmail.com"})
    assert response.status_code == 200
    assert EmailValidatorOut(**response.json())

def test_02_login():
    response = client.post("/api/v1/login", json={"email": "umair@gmail.com","password":"admin"})
    assert response.status_code == 200
    response = response.json()
    access_token = response['access_token']
    refresh_token = response['refresh_token']
    TestVariables.access_token = access_token
    TestVariables.refresh_token = refresh_token

def test_03_refresh_token():
    response = client.post("/api/v1/refresh-token", headers={"Authorization": f"Bearer {TestVariables.refresh_token}"})
    assert response.status_code == 200

def test_04_token():
    response = client.get("/api/v1/test-token", headers={"Authorization": f"Bearer {TestVariables.access_token}"})
    assert response.status_code == 200