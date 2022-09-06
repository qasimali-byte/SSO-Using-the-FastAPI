from tests.production.api_v1.global_test_variables import TestVariables
from test_production import client

def test_01_login():
    response = client.post("/api/v1/login", json={"email": "umair@gmail.com","password":"admin"})
    assert response.status_code == 200
    response = response.json()
    access_token = response['access_token']
    refresh_token = response['refresh_token']
    TestVariables.access_token = access_token
    TestVariables.refresh_token = refresh_token
    assert response['roles'] == ['super-admin']

def test_02_login():
    response = client.post("/api/v1/login", json={"email": "syed@gmail.com","password":"admin"})
    assert response.status_code == 200
    response = response.json()
    access_token = response['access_token']
    refresh_token = response['refresh_token']
    TestVariables.access_token = access_token
    TestVariables.refresh_token = refresh_token
    assert response['roles'] == ['external user']

def test_03_login():
    response = client.post("/api/v1/login", json={"email": "qasim@gmail.com","password":"admin"})
    assert response.status_code == 200
    response = response.json()
    access_token = response['access_token']
    refresh_token = response['refresh_token']
    TestVariables.access_token = access_token
    TestVariables.refresh_token = refresh_token
    assert response['roles'] == ['practice-admin']