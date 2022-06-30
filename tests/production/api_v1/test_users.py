from test_production import client
from src.apis.v1.validators.users_validator import UsersValidatorOut
from tests.production.api_v1.global_test_variables import TestVariables



def test_get_list_superusers():
    login_data = {
        "email": "umair@gmail.com",
        "password": "admin",
    }
    r = client.post("/api/v1/login", json=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    response = client.get("/api/v1/users?limit=3&offset=1",headers=headers)
    assert response.status_code == 200
    assert UsersValidatorOut(**response.json())
    response = response.json()
    data = response['users_data'][-1]
    assert len(response['users_data']) == 3
    
    
    response = client.get("/api/v1/users?limit=2&offset=2",headers=headers)
    assert response.status_code == 200
    assert UsersValidatorOut(**response.json())
    response = response.json()
    assert response['users_data'][0] == data
    assert len(response['users_data']) == 2


def test_get_list_subadminusers():
    login_data = {
        "email": TestVariables.demo_sub_admin_email,
        "password": "admin",
    }
    r = client.post("/api/v1/login", json=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    response = client.get("/api/v1/users?limit=1&offset=1",headers=headers)
    assert response.status_code == 200
    assert UsersValidatorOut(**response.json())
    response = response.json()
    assert len(response['users_data']) == 1
    

def test_get_list_practiceadminusers():
    login_data = {
        "email": "qwe@gmail.com",
        "password": "admin",
    }
    r = client.post("/api/v1/login", json=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    response = client.get("/api/v1/users/?limit=1&offset=1", headers=headers)
    assert response.status_code == 200
    assert UsersValidatorOut(**response.json())
    response = response.json()
    print(response)
    assert len(response['users_data']) == 1
    