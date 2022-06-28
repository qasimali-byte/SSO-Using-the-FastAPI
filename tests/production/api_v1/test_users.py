from test_production import client
from src.apis.v1.validators.users_validator import UsersValidatorOut



def test_get_users_info(superuser_token_headers):
    response = client.get("/api/v1/users",headers=superuser_token_headers)
    assert response.status_code == 200
    assert UsersValidatorOut(**response.json())
