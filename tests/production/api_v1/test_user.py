from src.apis.v1.validators.user_validator import UserInfoValidator, UserSPPracticeRoleValidatorOut, UserValidatorOut
from test_production import client

def test_get_user_info(superuser_token_headers):
    response = client.get("/api/v1/user",headers=superuser_token_headers)
    assert response.status_code == 200
    assert UserInfoValidator(**response.json())

def test_update_user_info(superuser_token_headers):
    json_data = { 
        "first_name": "Umair",
        "last_name": "Khan",
        "contact_no": "123456789",
        "address": "Somewhere"
        }
    response = client.put("/api/v1/user",headers=superuser_token_headers,json=json_data)
    assert response.status_code == 201
    assert UserInfoValidator(**response.json())

def test_get_user_practice_roles(superuser_token_headers):
    response = client.get("/api/v1/user/service-providers/practices/roles",headers=superuser_token_headers)
    assert response.status_code == 200
    assert UserSPPracticeRoleValidatorOut(**response.json())

def test_create_internal_user(superuser_token_headers):
    from tests.production.api_v1.user_json_testdata import data
    data["type_of_user"] = "internal"
    data["apps"].append(
            {
            "id": 7,
            "practices": [],
            "role": {
                    "id": 1,
                    "sub_role": None
                }
                
            },
    )
    response = client.post("/api/v1/user",headers=superuser_token_headers, json=data)
    assert response.status_code == 201
    assert UserValidatorOut(**response.json())

def test_create_external_user(superuser_token_headers):
    from tests.production.api_v1.user_json_testdata import data
    data["type_of_user"] = "external"
    response = client.post("/api/v1/user",headers=superuser_token_headers, json=data)
    assert response.status_code == 201
    assert UserValidatorOut(**response.json())