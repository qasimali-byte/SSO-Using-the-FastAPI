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
    response = client.get("/api/v1/users?limit=2&offset=2",headers=headers)
    assert response.status_code == 200
    assert UsersValidatorOut(**response.json())
    response = response.json()
    # assert response['users_data'][0] == data
    # assert len(response['users_data']) == 2 
    

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

def test_get_asc_des_first_last_id_name_list_superusers():
    login_data = {
        "email": "umair@gmail.com",
        "password": "admin",
    }
    r = client.post("/api/v1/login", json=login_data)
    '''
    Test Number of Superusers in per page Pass
    '''
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    response = client.get("/api/v1/users?limit=10&offset=1&order_by=first_name&latest=true",headers=headers)
    assert response.status_code == 200
    assert UsersValidatorOut(**response.json())
    response = response.json()
    data = response['users_data'][-1]
    assert len(response['users_data']) == 10
    assert response['users_data'][0]['first_name'] =='Asad'

    response = client.get("/api/v1/users?limit=10&offset=1&order_by=first_name&latest=false",headers=headers)
    assert response.status_code == 200
    assert UsersValidatorOut(**response.json())
    response = response.json()
    data = response['users_data'][-1]
    assert len(response['users_data']) == 10
    assert response['users_data'][0]['first_name'] =='wqwe'


    response = client.get("/api/v1/users?limit=10&offset=1&order_by=last_name&latest=true",headers=headers)
    assert response.status_code == 200
    assert UsersValidatorOut(**response.json())
    response = response.json()
    data = response['users_data'][-1]
    assert len(response['users_data']) == 10
    assert response['users_data'][0]['last_name'] =='Abbas'



    response = client.get("/api/v1/users?limit=10&offset=1&order_by=last_name&latest=false",headers=headers)
    assert response.status_code == 200
    assert UsersValidatorOut(**response.json())
    response = response.json()
    data = response['users_data'][-1]
    assert len(response['users_data']) == 10
    assert response['users_data'][0]['last_name'] =='User'

    response = client.get("/api/v1/users?limit=10&offset=1&order_by=id&latest=true",headers=headers)
    assert response.status_code == 200
    assert UsersValidatorOut(**response.json())
    response = response.json()
    data = response['users_data'][-1]
    assert len(response['users_data']) == 10
    assert response['users_data'][0]['id'] == 649

    response = client.get("/api/v1/users?limit=10&offset=1&order_by=id&latest=false",headers=headers)
    assert response.status_code == 200
    assert UsersValidatorOut(**response.json())
    response = response.json()
    data = response['users_data'][-1]
    assert len(response['users_data']) == 10
    assert response['users_data'][0]['id'] == 1819